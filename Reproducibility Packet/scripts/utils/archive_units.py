"""Read one probe's band units out of a processed IBL NWB file, over range requests.

``utils.band_drift`` defines the drift statistic that gates a Tier A host, and it
takes per-unit spike times and per-spike depths as plain arrays. This module is
what puts real arrays in front of it: it opens a processed NWB blob over HTTP
range requests and reads the ragged ``spike_times`` and
``spike_distances_from_probe_tip_um`` slices belonging to the units whose peak
electrode sits inside a pinned anatomical band -- and nothing else in the file.

**Targeted, because the alternative is the whole sorting.** The two ragged
columns hold every spike of every unit on every probe. A candidate's band holds
22 to 267 units out of many hundreds, so resolving each band unit's slice from
the column's own index and reading only that slice is the difference between a
few hundred megabytes and the entire sorting. The index arrays are one integer
per unit and are read in full, so every slice is known before any of them is
read and :func:`plan_transfer` can size the read before it happens.

**Several byte counts, because the read is paid for in more than one currency
and the parts of it are live at the same time.** The count this module first
reported was the stored payload of the slices, and a ceiling enforced on it
bounded neither what the read transfers nor what it holds. A range-request
reader fetches whole fixed-size blocks and *keeps* them -- its cache is
unbounded and lives until the read returns -- so a scattered slice can cost a
block or more of transfer for a few kilobytes of payload, and those blocks are
still resident when the arrays they fed are resident too. The arrays are
converted to float64 on the way in, so what is held is not what is stored
either. :func:`plan_transfer` therefore reports ``logical_bytes`` (the stored
payload, exact), ``cache_bound_bytes`` (an upper bound on the distinct block
bytes the read can fetch, including what has already been spent on metadata),
``resident_bytes`` (the converted arrays plus the largest slice at its stored
width) and ``structures_bytes`` (a measured bound on the Python containers the
read holds while it runs). ``peak_resident_bytes`` is the sum of the last
three, and it is the single quantity :func:`read_band_units` enforces its
ceiling against, because those three are live together rather than in turn.

**The block bound is derived from where the bytes actually are.** A contiguous
dataset whose file offset h5py will give is placed exactly. A chunked dataset is
placed from the file byte range of every chunk the slices touch, read from the
chunk index, because HDF5 does not promise that successive chunks occupy one
contiguous span -- an earlier version assumed they did, and on a file whose
chunks are interleaved with other data it under-bounded the transfer by a
quarter. Where neither route is available the bound is the whole file, which is
loose but is the only thing still true. ``bound_basis`` names which routes a
given plan used.

**Every read this module performs happens before that bound is computed, except
the per-unit slices the bound is about.** The electrode table, the unit scalars,
the column descriptions, the conversion provenance, the two column layouts and
the chunk index are all read while the reader's spend is still being counted, so
each of them lands inside ``spent_bytes`` and therefore inside the bound. The
provenance read used to sit *after* the ceiling was enforced, where it was
invisible to the plan and could transfer megabytes a caller had been told would
not be transferred; the rule the repair leaves behind is the general one, and it
is what the harness now checks on every fixture that performs a read.

**Accounted is not bounded, and a request is not a transfer.** Those are two
distinct repairs and the module needed both. Moving the provenance read into
preflight made its cost appear in the plan, but the plan is written after the
read: a two-million-character variable-length value was still transferred in
full and only then reported, so the number a caller was given was honest about a
spend that had already happened. HDF5 will not state such a value's size in
advance, but it does *ask this module's reader* for the bytes before they move,
so :class:`BoundedReader` refuses the request rather than measuring the result.
That bounded what the read asks for -- and not what the read costs. The reader
underneath fetches whole blocks, so at a 1 MiB block a sixteen-byte request for
an unfetched byte spends a mebibyte, and a budget of 65,536 bytes stated as the
most one path could spend was unreachable rather than merely unenforced. The
proxy therefore models the block cache and charges each read the distinct bytes
it would newly fetch, against a second budget denominated in blocks and derived
in :func:`provenance_transfer_budget`. **Both budgets refuse before delegating,
and both are reported beside what they actually spent**, so ``--plan-only``
states the bound before the run rather than the spend after it.

**Two provenance paths are authenticated rather than recorded, and one of them
has to agree across the pair.** The session-time origin the drift grid is
anchored on is a property of the converter and of the file's own declared
reference instant, so an asset that states neither cannot establish it.
``general/source_script`` must be present, must have been read whole, and must
*be* the conversion statement the measured assets carry -- matched end to end,
because a search for the tool's name alone said yes to a value reading "NOT
created using NeuroConv", and a negated occurrence is not provenance. The root
``timestamps_reference_time`` must be present, read whole, and parse as a
timezone-aware ISO-8601 instant, and the two halves of one session must denote
the **same** instant, because NWB defines every time value in a file as seconds
counted from that instant and two different origins are two coordinates.

**The pair used to be required to name the same converter version, and that
rule admitted nothing.** It was measured across 71 sessions of DANDI 000409 --
the 11 distinct sessions of the pinned candidate order and a deterministic
60-session holdout drawn from the other 448 -- and every raw asset was written
by NeuroConv 0.9.1 or 0.9.2 while every processed asset was written by 0.9.4.
Agreement was 0 of 71. The property it stood in for is readable directly and
behaves differently: the declared reference instants agree exactly on 63 of
those 71 and differ by exactly one hour on 8, and those 8 carry the *same*
version pair as the 63. A proxy that admits none of the real population, and
that cannot see the defect it stands in for, is not a conservative check. The
versions are still parsed, still reported, and no longer vote. What these checks
can and cannot establish is written at :data:`REQUIRED_PROVENANCE_PATH`,
:data:`REFERENCE_TIME_PATH` and :func:`authenticate_provenance_pair`, and the
honest half of it is that no asset in this dandiset carries the conversion
repository's commit, so no check here confirms it -- and that agreeing reference
instants are a necessary declared condition rather than an identification of the
clock.

**What it validates, and why validation lives here rather than in the caller.**
Four properties have to hold before a drift number computed from these arrays
means anything, and every one of them is a property of the file rather than of
the statistic:

1. the two ragged columns are partitioned identically, by offsets that are
   stored as integers, so that a unit's times and its depths are the same
   spikes in the same order;
2. the loaded values are finite, each unit's times ascend, and the depth column
   still carries its documented micrometre unit;
3. each unit's ``max_electrode`` -- also an integer as stored -- names exactly
   one electrode on that unit's own probe, and that electrode's ``rel_y`` is
   finite;
4. the processed file's electrode table agrees with the raw file's, because the
   band is derived from the raw table while ``max_electrode`` indexes the
   processed one.

**The structural columns are checked as stored, before anything converts them.**
``int()`` accepts a float and truncates it, so two ragged indices differing by
less than one, or an electrode reference that is not a whole number, would have
been read as a well-formed partition and as a valid row. Integrality and dtype
are therefore confirmed on the stored values, and every one-value-per-unit
column is required to hold one value per unit, before a single row is resolved.

**The two ragged indices are held to a stricter rule than the electrode
reference, because the schema is stricter about them.** ``spike_times_index``
and its depth counterpart are HDMF ``VectorIndex`` datasets, and the common
schema specifies unsigned-integer storage for them, so a floating-point index is
a malformed file rather than a permissible encoding -- integral values do not
make it well formed. Those two are required to be stored in an integer dtype.
``max_electrode`` is a custom IBL column that the schema does not type, so a
float column whose values are exactly whole is accepted there and its stored
dtype is reported. The asymmetry is deliberate and is the difference between
enforcing a specification and inventing one.

A violation of any of these raises :class:`ValueError`. That is deliberate and it
matters for the host order: a candidate whose *inputs* are malformed has not
failed the drift gate, and recording it as a drift failure would hand the host
to the next rank for a reason that has nothing to do with drift.

Nothing here computes, thresholds, or interprets a drift value. This module
reads and checks; ``utils.band_drift`` measures.
"""

import contextlib
import datetime
import io
import re
import sys

import numpy as np

import h5py

from utils.remote_hdf5 import RemoteFile

UNITS_PATH = "units"
ELECTRODES_PATH = "general/extracellular_ephys/electrodes"
TIME_COLUMN = "spike_times"
DEPTH_COLUMN = "spike_distances_from_probe_tip_um"

# The depth column's own first-party description is the only statement in the
# file about what unit its values carry. Requiring this substring keeps the
# check first-party without turning a punctuation difference into a rejection;
# the whole description is reported verbatim beside the verdict.
DEPTH_UNIT_PHRASE = "micrometers"

# The conversion provenance the selection document's clock claim rests on. The
# session-time origin is a property of the converter, not of the recorded
# arrays, so the asset's own statement of what produced it is the only
# asset-level evidence that this file came off the documented conversion path --
# and the file's own declared reference instant is the only asset-level evidence
# of where its time values are counted from.
#
# **The two authenticated paths are read first, in that order.** The budget is
# cumulative over the whole call, so a path read after an expensive one may find
# nothing left; putting both required paths ahead of the recorded ones is what
# makes the budget unable to starve a verdict.
#
# **``general/session_start_time`` was here and is not any more.** It is absent
# from all 142 assets read across the 71 sessions measured in Session 33, so it
# contributed nothing but one block of stated transfer budget. The value NWB
# actually defines sits at the file root, and the root ``session_start_time`` is
# present on all 142 and equal to ``timestamps_reference_time`` on all 142 -- it
# is recorded here for the reader, and nothing gates on it.
PROVENANCE_PATHS = (
    "general/source_script",
    "timestamps_reference_time",
    "session_start_time",
    "general/institution",
    "general/lab",
)

# The one path that is required rather than recorded, and the pinned token its
# value is authenticated against.
#
# **What this authenticates, and what it cannot.** Session 7 read /general from
# one raw NWB per subject across 21 assets of DANDI 000409 -- the donor
# library's 12 subjects and the 9 that own the current candidate hosts -- and
# every one carried general/source_script, reading "Created using NeuroConv
# v0.9.2" on 20 of them and "v0.9.1" on the remaining one
# (results/subject_provenance.json). So the toolchain token is checkable against
# a measurement rather than against an assumption. The pinned *commit* of
# catalystneuro/IBL-to-nwb is not: no asset in that survey carries it, so no
# check here can confirm it, and pretending otherwise would be the check
# claiming more than it does. What this rule establishes is that the asset
# states it was produced by the documented conversion toolchain; that the
# toolchain at the pinned commit exports the shared session-time coordinate is
# the selection document's claim about the repository and stays there.
REQUIRED_PROVENANCE_PATH = "general/source_script"
CONVERSION_SOURCE_TOKEN = "neuroconv"

# The second required path: the instant the file's time values are counted from.
#
# **What the format says it is.** The NWB specification defines
# ``timestamps_reference_time`` on ``NWBFile`` as the reference time for every
# timestamp in the file -- each stored time value is seconds relative to it --
# and defaults it to ``session_start_time``. It is therefore not a description
# of the recording, it is the origin of the coordinate the bin grid is laid on,
# and it is stated by the file rather than inferred from it.
#
# **What was measured, and why this path replaced a proxy.** Session 33 read
# both halves of 71 sessions of DANDI 000409 -- the 11 distinct sessions of the
# pinned candidate order plus a deterministic 60-session holdout drawn from the
# other 448, so the holdout excludes the sessions the hypothesis was formed on.
# Every asset carried this path and carried it as a timezone-aware ISO-8601
# value; ``session_start_time`` equalled it on all 142. Processed minus raw was
# exactly ``+0.0 s`` on 63 sessions and exactly ``+3600.0 s`` on 8, and never
# anything else. The 8 are all one laboratory's sessions inside the US-Eastern
# daylight window. **That is a described pattern and not a measured mechanism**:
# a daylight-saving handling difference between the two conversion passes fits
# every number, no mechanism was measured, and none is claimed here.
#
# **What agreement here does and does not establish.** It is a necessary
# declared condition: two assets that name different origins are not stating one
# coordinate, whatever their arrays contain. It is not an identification of the
# clock, for the same reason endpoint containment is not one -- both halves could
# agree on a declared origin and still have been written with different internal
# conventions. The evidence set for the shared clock stays what the selection
# document's section 16.4 says it is: the pinned converter commit's semantics,
# each asset's own conversion statement, this agreement, and containment as a
# consistency check with stated slack.
REFERENCE_TIME_PATH = "timestamps_reference_time"

# The positive form the measured values take, matched end to end rather than
# searched for. Searching for the token above is not authentication: a value
# reading "This asset was NOT created using NeuroConv; exported by LocalTool v3"
# contains the token and denies the statement, so the search answered yes to a
# file that says no. A negated occurrence is not provenance. The whole value
# must be the sentence all 21 measured assets carry -- case-insensitively, and
# with surrounding whitespace stripped, because a rejection on capitalisation
# or on a trailing newline would be a rejection on typography -- and the
# version it names is captured rather than matched against a list.
CONVERSION_SOURCE_FORM = re.compile(
    r"^created using neuroconv v(?P<version>\d+(?:\.\d+)*)$")
CONVERSION_SOURCE_FORM_TEXT = "Created using NeuroConv v<version>"

# The lexical form a reference time must take before it is parsed at all.
#
# **Why a grammar and not just the parser.**
# :meth:`datetime.datetime.fromisoformat` is deliberately more permissive
# than ISO-8601 on the pinned interpreter (CPython 3.12.10): it accepts any
# single character in the date/time separator's place, so
# ``2021-05-10Q14:33:49.023776-04:00`` parses, carries an offset, and used
# to reach a drift verdict. NWB states
# this field as an ISO-8601 timestamp, and a value that is not one is a
# malformed input rather than a clock this command may read. The parser is
# still what validates the *values* -- month 13, hour 25, 31 February -- so
# this expression only has to bound the shape.
#
# **What it admits, measured rather than chosen.** All 142 assets read
# across the 71 sessions of Session 33's census carry exactly four shapes:
# ``YYYY-MM-DDThh:mm:ss[.ffffff]`` followed by ``+hh:mm`` or ``-hh:mm``.
# This expression is deliberately a little wider than that population --
# seconds may be omitted, the fraction may be any number of digits, ``Z``
# and a whole-hour offset are accepted -- because those are ISO-8601
# extended forms a later converter could legitimately emit, and refusing
# one would be the pessimistic mirror of the defect this card repairs. It
# does not accept the basic-format offset ``+hhmm``. ISO-8601 requires the
# date and time halves of one representation to use the same format, basic
# or extended; applying that consistency to the offset as well is a reading
# rather than a quoted clause, it is stated here rather than defended, and
# no measured asset spells its offset that way.
#
# **The offset is not required here.** It is required one line below, by
# the parsed value carrying a ``utcoffset``, so that the shape rule and the
# offset rule stay one enforcer each rather than two enforcers of one
# property that no single change could ever defeat.
REFERENCE_TIME_FORM = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?"
    r"(?:Z|[+-]\d{2}(?::\d{2})?)?\Z")
REFERENCE_TIME_FORM_TEXT = "YYYY-MM-DDThh:mm[:ss[.ffffff]][+/-]hh:mm"

# The versions that measurement found: reported, and deliberately NOT gated on.
#
# **The list grew because the measurement did, and the growth is the whole
# story.** Session 7 read one *raw* asset per subject across 21 assets and found
# 0.9.2 on twenty and 0.9.1 on one. Nothing had ever read a *processed* asset's
# statement. Session 33 read both halves of 71 sessions: raw 0.9.1 once and
# 0.9.2 seventy times, processed 0.9.4 on all seventy-one. So the dandiset is
# not uniform in its converter version, the two halves of a session are never
# converted by the same version, and a rule requiring them to agree admitted 0
# of 71 -- see :func:`authenticate_provenance_pair` for what replaced it.
#
# Gating on this tuple would still be wrong for the reason it always was: it is
# a list taken from the assets this project happens to have read, and a fourth
# version is not by itself evidence of a different clock. What is gated is the
# form above, which all 142 measured assets satisfy, and the declared reference
# instant, which is the property the common-clock claim actually needs.
MEASURED_CONVERSION_VERSIONS = ("0.9.1", "0.9.2", "0.9.4")

# The budget on what reading conversion provenance may *ask for*, and so on what
# it may materialize, cumulative across the whole call. Pinned here rather than
# passed in, because a value read from a candidate must not be able to choose
# the number that decides whether reading it was allowed. It is deliberately far
# above any plausible real value -- the measured values are about thirty
# characters -- and a refused read spends none of it, so one oversized value
# does not stop the paths after it from being read.
PROVENANCE_MAX_BYTES = 65536

# The block size the *raw* asset's provenance read uses, capped below whatever
# the caller passed. That read is the one with no *plan* behind it -- there is
# no band to size and nothing to compare a footprint against -- so its transfer
# bound should not scale with a block size chosen for a bulk payload read on a
# different file. At 64 KiB the bound is 393,216 bytes instead of the 5,308,416
# a 1 MiB block would make it. Since RC-004-F2 the caller's declared ceiling is
# held open around that read as well, so this bound is the inner of two and not
# the only one.
PROVENANCE_BLOCK_BYTES = 65536

# Labels for the two nested read budgets, so a refusal says which one
# refused. They are constants because :func:`source_provenance`'s handler
# compares against one of them, and a handler that compared against a literal
# would silently stop matching if the label were reworded.
PROVENANCE_SCOPE = "provenance"
PREFLIGHT_SCOPE = "declared ceiling"

# The two self-describing forms a provenance value can take when it was not read
# whole. They are prefixes rather than free text so that
# :func:`provenance_is_complete` can decide the question mechanically, and so
# that an authentication can refuse to run on a value it did not fully see.
PROVENANCE_UNREAD_PREFIX = "<not read:"
PROVENANCE_TRUNCATED_PREFIX = "<truncated:"


def provenance_transfer_budget(block_bytes):
    """Return the distinct-transfer budget for one conversion-provenance read.

    **Why there is a second budget at all.** :data:`PROVENANCE_MAX_BYTES`
    bounds the request; it does not bound the transfer that serves the
    request, because the reader underneath fetches whole fixed-size blocks.
    At the command's default 1 MiB block a sixteen-byte read of a byte
    nothing has fetched yet costs a whole mebibyte, and a
    two-million-character value under a 65,536-byte request budget moved
    2,081,456 distinct bytes -- essentially the whole generated file --
    before the refusal. At that block size the stated number was not merely
    unenforced, it was unreachable: nothing can be read for less than one
    block.

    **The value is derived rather than chosen: the request budget, plus one
    block per provenance path.** The first term is what proves a legal value
    can always be read wherever it sits -- a value of at most ``C`` bytes
    starting at an arbitrary offset spans at most ``ceil(C / B) + 1`` blocks,
    which is at most ``C + 2B`` bytes -- and the second leaves ``2B`` over
    for the object headers, heap collections and group links that reach the
    four paths. The result cannot be smaller than one block, and that is a
    property of the caller's ``--block-kb`` rather than of this rule.

    Args:
        block_bytes: the reader's block size, or 0 when it fetches exactly
            what it is asked for.

    Returns:
        The budget in bytes, or None for a reader that does not fetch in
        blocks -- there the transfer equals the request and
        :data:`PROVENANCE_MAX_BYTES` already bounds it, so a second budget
        would be the same number under another name.
    """
    if not block_bytes:
        return None
    return PROVENANCE_MAX_BYTES + len(PROVENANCE_PATHS) * int(block_bytes)


class ReadBudgetExceeded(ValueError):
    """Raised when a read would spend more than a budget in force allows.

    It is a :class:`ValueError` because every other statement this module makes
    about a malformed or oversized asset is one, and :func:`read_band_units`'s
    caller converts that class into an input error rather than a drift verdict.

    Attributes:
        scope: which budget refused, since budgets nest. A refusal by the
            provenance budget is a statement about one value and is recorded as
            a marker; a refusal by the ceiling is a statement about the whole
            read and must not be swallowed by the code handling the former.
            Without this the two are one exception type and the inner handler
            catches both.
    """

    def __init__(self, message, scope=None):
        """Record the refusing scope's label alongside the message."""
        ValueError.__init__(self, message)
        self.scope = scope


class BoundedReader(io.RawIOBase):
    """A transparent proxy over a range reader that can refuse a read before it happens.

    **Why a proxy rather than a size check.** HDF5 will state the stored size of
    a fixed-length value, so an oversized one can be refused by asking. It will
    not state the size of a variable-length string: the characters live in the
    global heap and the dataset stores only heap references, so h5py 3.16.0
    reports 16 bytes of storage for a 4.2 MB value. Asking is therefore not
    available for the representation IBL actually uses, and an accounting repair
    -- moving the read to where the plan can count it -- makes the spend
    *visible* without making it *refusable*. What is still available is the
    request: h5py asks this object for the heap collection's bytes before they
    move, so a proxy that checks the requested length and raises can decline the
    read before those bytes move.

    **Two budgets, because a request and the transfer that serves it are not the
    same size.** Charging only the requested length bounds what is
    *materialized* and not what is *transferred*: the reader underneath fetches
    whole fixed-size blocks and keeps them, so a sixteen-byte read of a byte
    nothing has fetched yet costs a whole block. Measured on a
    two-million-character value under a 65,536-byte request budget at a 1 MiB
    block, 2,081,456 distinct bytes moved before the refusal. This proxy
    therefore models the reader's block cache: before delegating any read it
    computes which blocks that read would *newly* fetch, charges their whole
    size against a second, transfer-denominated budget, and refuses rather than
    delegating when the charge does not fit.

    **Why the model is exact, and conservative where it is not.** Every read
    h5py makes on this file goes through this object, and a block-caching reader
    fetches exactly the blocks covering the range it is asked for, so the set of
    blocks recorded here is the set the reader holds. A refused read spends
    nothing and is recorded as fetching nothing. A read is charged for the range
    it requests, clamped to the file's size the way the reader clamps it, and
    the blocks it marks as fetched are the same clamped range -- so the model
    never credits the cache with a block the reader did not fetch.

    A reader that declares no block size does not expand a read: its transfer is
    its request, and the request budget already bounds it. The attributes the
    model reads are ``block`` and ``size``, both of which
    :class:`utils.remote_hdf5.RemoteFile` publishes.

    The proxy is transparent when no budget is in force, which is every read
    outside :func:`source_provenance`. It forwards the reader's own counters, so
    a caller reads ``n_bytes`` and ``n_requests`` from either object and gets
    the same numbers.

    Attributes:
        n_bytes: the wrapped reader's transferred-byte counter.
        n_requests: the wrapped reader's request counter.
        block_bytes: the wrapped reader's block size, or 0 if it declares none.
        last_spend: what the most recently closed budget block spent, as a dict
            of both budgets and both amounts. It is how a caller reports a bound
            and the spend inside it without reaching into this object's state.
    """

    def __init__(self, inner):
        """Wrap ``inner``, which must be a seekable binary reader."""
        self._inner = inner
        self._block = int(getattr(inner, "block", 0) or 0)
        self._size = int(getattr(inner, "size", 0) or 0)
        self._fetched = set()
        self._scopes = []
        self.last_spend = None

    @property
    def block_bytes(self):
        """The wrapped reader's block size, or 0 when it fetches what it is asked for."""
        return self._block

    @contextlib.contextmanager
    def budget(self, read_bytes, transfer_bytes=None, label="budget"):
        """Refuse, inside this block, any read that would exceed either budget.

        **Budgets nest, and every enclosing one is charged.** The provenance
        read sits inside the ceiling the caller declared, and a scheme where the
        inner budget replaced the outer would leave the outer blind to exactly
        the reads the inner one permitted. Each scope keeps its own pair of
        remainders; a read is refused unless it fits in all of them, and it is
        charged to all of them only once it has.

        Args:
            read_bytes: the budget on what may be asked for, and therefore on
                what may be materialized, covering every read made inside the
                block. None bounds nothing, for a scope that only bounds
                transfer.
            transfer_bytes: the budget on the distinct bytes the reader
                underneath may newly fetch. None means the request is the
                transfer, which is true of a reader that declares no block size.
            label: what to name this scope when it is the one that refuses, so a
                handler for one budget's refusals does not silently absorb
                another's.

        Yields:
            None. On exit this scope is removed whether or not the block raised,
            and ``last_spend`` records what it spent against each of its
            budgets.
        """
        limit = read_bytes if transfer_bytes is None else transfer_bytes
        scope = {
            "label": label,
            "read_budget": None if read_bytes is None else int(read_bytes),
            "read_remaining": None if read_bytes is None else int(read_bytes),
            "transfer_budget": None if limit is None else int(limit),
            "transfer_remaining": None if limit is None else int(limit),
        }
        self._scopes.append(scope)
        try:
            yield
        finally:
            self._scopes.pop()
            self.last_spend = {
                "label": scope["label"],
                "read_budget_bytes": scope["read_budget"],
                "read_bytes": (None if scope["read_budget"] is None
                               else scope["read_budget"] - scope["read_remaining"]),
                "transfer_budget_bytes": scope["transfer_budget"],
                "transfer_bytes": (None if scope["transfer_budget"] is None
                                   else scope["transfer_budget"]
                                   - scope["transfer_remaining"]),
                "block_bytes": self._block,
            }

    def _block_span(self, position, n_bytes):
        """Return the block indices a read of ``n_bytes`` at ``position`` would fetch."""
        if not self._block or self._size <= 0:
            return ()
        length = min(n_bytes, max(0, self._size - position))
        if length <= 0:
            return ()
        return range(position // self._block,
                     (position + length - 1) // self._block + 1)

    def _block_size(self, index):
        """Return how many bytes block ``index`` holds; the last one is short."""
        return max(0, min(self._block, self._size - index * self._block))

    def _transfer_cost(self, position, n_bytes):
        """Return the distinct bytes a read at ``position`` would newly fetch."""
        if not self._block:
            return min(n_bytes, max(0, self._size - position))
        return sum(self._block_size(index)
                   for index in self._block_span(position, n_bytes)
                   if index not in self._fetched)

    def _charge(self, n_bytes):
        """Refuse or account for a read of ``n_bytes`` before it is delegated.

        Every enclosing scope is tested before any of them is charged, so a
        refusal leaves every budget exactly as it was and nothing moves.
        """
        position = self._inner.tell()
        wanted = self._size if n_bytes is None or n_bytes < 0 else n_bytes
        if not self._scopes:
            self._fetched.update(self._block_span(position, wanted))
            return
        cost = self._transfer_cost(position, wanted)
        for scope in reversed(self._scopes):
            if scope["read_remaining"] is not None:
                if n_bytes is None or n_bytes < 0:
                    raise ReadBudgetExceeded(
                        "a read to end-of-file was requested under a %d-byte %s read "
                        "budget" % (scope["read_budget"], scope["label"]),
                        scope["label"])
                if n_bytes > scope["read_remaining"]:
                    raise ReadBudgetExceeded(
                        "a %d-byte read exceeds the %d bytes left of a %d-byte %s read "
                        "budget" % (n_bytes, scope["read_remaining"],
                                    scope["read_budget"], scope["label"]),
                        scope["label"])
            if scope["transfer_remaining"] is not None and cost > scope["transfer_remaining"]:
                raise ReadBudgetExceeded(
                    "a %d-byte read at offset %d would transfer %d distinct bytes at the "
                    "reader's %d-byte block size, and %d bytes are left of a %d-byte %s "
                    "transfer budget; the size of a request is not the size of the "
                    "transfer that serves it"
                    % (n_bytes, position, cost, self._block,
                       scope["transfer_remaining"], scope["transfer_budget"],
                       scope["label"]),
                    scope["label"])
        for scope in self._scopes:
            if scope["read_remaining"] is not None:
                scope["read_remaining"] -= n_bytes
            if scope["transfer_remaining"] is not None:
                scope["transfer_remaining"] -= cost
        self._fetched.update(self._block_span(position, wanted))

    def readable(self):
        """Return True; this proxy is read-only."""
        return True

    def seekable(self):
        """Return True; h5py seeks constantly."""
        return True

    def writable(self):
        """Return False; nothing here writes."""
        return False

    def seek(self, offset, whence=io.SEEK_SET):
        """Seek the wrapped reader. Seeking spends nothing and is never refused."""
        return self._inner.seek(offset, whence)

    def tell(self):
        """Return the wrapped reader's position."""
        return self._inner.tell()

    def read(self, n=-1):
        """Read ``n`` bytes, refusing before delegating when a budget forbids it."""
        self._charge(n)
        return self._inner.read(n)

    def readinto(self, buffer):
        """Read into ``buffer``, refusing before delegating when a budget forbids it."""
        self._charge(len(buffer))
        return self._inner.readinto(buffer)

    def close(self):
        """Close the wrapped reader, then this proxy."""
        try:
            self._inner.close()
        finally:
            super(BoundedReader, self).close()

    @property
    def n_bytes(self):
        """The wrapped reader's transferred-byte counter."""
        return self._inner.n_bytes

    @property
    def n_requests(self):
        """The wrapped reader's request counter."""
        return self._inner.n_requests


def ascii_safe(text, limit=200):
    """Return an ASCII-only, length-limited rendering of a value read from a file.

    Args:
        text: the decoded value.
        limit: how many characters to keep.

    Returns:
        The value with every non-ASCII character escaped and the tail replaced
        by an ellipsis when it was longer than ``limit``. Provenance strings
        come from the asset rather than from this project, and both the report
        and this console are ASCII-only, so a value is rendered rather than
        printed.
    """
    clipped = text[:limit]
    safe = clipped.encode("ascii", "backslashreplace").decode("ascii")
    return safe if len(text) <= limit else safe + "..."


def _decode(values):
    """Decode an h5py string column into a list of str.

    Args:
        values: an h5py dataset slice holding bytes or str.

    Returns:
        A list of Python strings.
    """
    return [v.decode() if isinstance(v, bytes) else str(v) for v in values]


def read_flat_electrodes(handle):
    """Read one NWB file's electrode table as flat, globally indexed columns.

    ``max_electrode`` is a row index into this table, so the table has to be
    read flat. ``utils.host_anatomy.read_electrode_table`` groups the same rows
    by probe, which is the right shape for finding a band and the wrong shape
    for resolving a row index.

    Args:
        handle: an open :class:`h5py.File`.

    Returns:
        A dict with ``rel_y`` (list of float), ``group_name`` and ``location``
        (lists of str), all of length ``n_rows``, plus ``n_rows``.

    Raises:
        KeyError: if the file carries no electrode table, which is a malformed
            asset rather than an absent measurement.
    """
    if ELECTRODES_PATH not in handle:
        raise KeyError("file has no %s" % ELECTRODES_PATH)
    table = handle[ELECTRODES_PATH]
    rel_y = [float(v) for v in table["rel_y"][:]]
    return {
        "rel_y": rel_y,
        "group_name": _decode(table["group_name"][:]),
        "location": _decode(table["location"][:]),
        "n_rows": len(rel_y),
    }


def column_descriptions(handle, columns=(TIME_COLUMN, DEPTH_COLUMN)):
    """Read the units table's own description attribute for named columns.

    Args:
        handle: an open :class:`h5py.File`.
        columns: column names to describe.

    Returns:
        A dict from column name to its stored description, or to None where the
        column carries no description attribute.
    """
    node = handle[UNITS_PATH]
    out = {}
    for name in columns:
        if name not in node:
            out[name] = None
            continue
        value = node[name].attrs.get("description")
        if isinstance(value, bytes):
            value = value.decode()
        out[name] = str(value) if value is not None else None
    return out


def _stored_value_bytes(node):
    """Return a dataset's stored payload size in bytes, or None if HDF5 will not say.

    Args:
        node: whatever :meth:`h5py.File.__getitem__` returned for the path.

    Returns:
        The stored size in bytes, or None when there is no honest pre-read
        answer. A variable-length string is the case that matters: its
        characters live in HDF5's global heap and the dataset itself stores only
        the heap references, so on h5py 3.16.0 a 4,200,030-character value
        reports 16 bytes of storage and 8 bytes of ``nbytes``. Returning either
        as a size would be a fiction, and a fictional bound is worse than an
        absent one.
    """
    if not isinstance(node, h5py.Dataset):
        return None
    info = h5py.check_string_dtype(node.dtype)
    if info is not None and info.length is None:
        return None
    try:
        return int(node.id.get_storage_size())
    except (AttributeError, ValueError, RuntimeError):
        return None


def _capped(text, max_bytes):
    """Return ``text`` if it is within the cap, or a truncated, self-describing form.

    Args:
        text: the decoded value.
        max_bytes: the cap, applied here to characters. A UTF-8 character is at
            least one byte, so this never retains fewer bytes than the cap
            names, and at most four times it. The exact retained size is
            measured rather than assumed: the returned dict is charged into
            ``structures_bytes`` by :func:`plan_transfer`.

    Returns:
        The text, or its first ``max_bytes`` characters followed by a marker
        naming the full length, so a reader can tell a short value from a
        truncated one.
    """
    if len(text) <= max_bytes:
        return text
    return ("%s%s %d characters read, %d-character provenance cap>"
            % (text[:max_bytes], PROVENANCE_TRUNCATED_PREFIX, len(text), max_bytes))


def source_provenance(handle, reader, max_bytes=PROVENANCE_MAX_BYTES):
    """Read the asset's conversion provenance under an enforced read budget.

    Args:
        handle: an open :class:`h5py.File`.
        reader: the :class:`BoundedReader` the file was opened on. It is
            required rather than optional. Without it a variable-length value
            cannot be refused before its bytes move, and an unbounded read of a
            value whose size HDF5 will not state is the exact defect this
            argument exists to prevent.
        max_bytes: the pinned budget on what this call may ask for, cumulative
            over every path, every attribute and every structural read inside
            it. The transfer budget is derived from the reader's own block size
            by :func:`provenance_transfer_budget`; both are readable afterwards
            from ``reader.last_spend`` together with what they spent.

    Returns:
        A dict from path to its stored value as a string, omitting paths the
        file does not carry. A value the budget refused, or whose stated stored
        size was already over the budget, is replaced by a marker beginning with
        :data:`PROVENANCE_UNREAD_PREFIX` that names what was refused and why, so
        a refusal is distinguishable from a short value and
        :func:`authenticate_provenance` can decline to authenticate on one.

    Note:
        **Two repairs live here and they are different repairs.** The first was
        one of accounting: this function was called after
        :func:`read_band_units` had enforced its memory ceiling, so a
        schema-valid file carrying a 4,200,030-character
        ``general/source_script`` was admitted under a 174,368-byte transfer
        bound and then transferred 4,232,336 bytes. Moving the call into
        preflight put those bytes inside ``spent_bytes`` and therefore inside
        the plan. But an accounted spend is not a refused one: with the read
        still unbounded, a two-million-character value was *spent* and only then
        reported, so the cost became visible without becoming preventable. The
        second repair is the budget, which refuses the read at the request
        rather than measuring it afterwards. **The third is that a request is
        not a transfer**: the budget above bounded what h5py asked for while
        the reader underneath fetched whole blocks, so a value refused under a
        65,536-byte budget still moved 2,081,456 distinct bytes at a 1 MiB
        block. The block-denominated budget is what closes that, and the reason
        one budget scope now covers the whole call rather than one read is that
        a per-read bound says nothing about the total a scattered file can cost.

        **A refused read spends neither budget**, so an oversized or unreachable
        value does not stop the paths after it from being read; and the two
        required paths are read first, so the budget is never consumed before
        the paths a verdict depends on have had it.
    """
    out = {}
    with reader.budget(max_bytes, provenance_transfer_budget(reader.block_bytes),
                       label=PROVENANCE_SCOPE):
        for path in PROVENANCE_PATHS:
            try:
                if path not in handle:
                    continue
                node = handle[path]
            except ReadBudgetExceeded as exc:
                # Resolving the path is itself a read, so it is inside the
                # budget rather than beside it. A bound that covered the value
                # and not the traversal that reaches it would be a bound on
                # part of the spend it names. Only this scope's refusals are
                # recorded as markers -- an enclosing budget refusing here is a
                # statement about the whole read and is re-raised.
                _own_refusal(exc)
                out[path] = "%s %s>" % (PROVENANCE_UNREAD_PREFIX, exc)
                continue
            stored = _stored_value_bytes(node)
            if stored is not None and stored > max_bytes:
                out[path] = ("%s %d stored bytes exceeds the %d-byte provenance budget>"
                             % (PROVENANCE_UNREAD_PREFIX, stored, max_bytes))
                continue
            try:
                value = node[()]
            except ReadBudgetExceeded as exc:
                _own_refusal(exc)
                out[path] = "%s %s>" % (PROVENANCE_UNREAD_PREFIX, exc)
                continue
            except (TypeError, ValueError):
                continue
            if isinstance(value, bytes):
                value = value.decode()
            out[path] = _capped(str(value), max_bytes)
            for key in ("file_name", "software", "version"):
                try:
                    attr = node.attrs.get(key)
                except ReadBudgetExceeded as exc:
                    _own_refusal(exc)
                    out["%s@%s" % (path, key)] = ("%s %s>"
                                                  % (PROVENANCE_UNREAD_PREFIX, exc))
                    continue
                if attr is None:
                    continue
                if isinstance(attr, bytes):
                    attr = attr.decode()
                out["%s@%s" % (path, key)] = _capped(str(attr), max_bytes)
    return out


def _own_refusal(exc):
    """Re-raise a budget refusal that belongs to an enclosing scope.

    Args:
        exc: the :class:`ReadBudgetExceeded` just caught.

    Raises:
        ReadBudgetExceeded: unmodified, when it was not the provenance budget
            that refused. A ceiling refusal recorded as "this value could not be
            read" would turn a statement about the whole read into a marker
            beside one path, which is a failure that reports itself as a
            success.
    """
    if getattr(exc, "scope", None) != PROVENANCE_SCOPE:
        raise exc


def provenance_is_complete(value):
    """Return True when a provenance value was read whole rather than refused or capped.

    Args:
        value: one entry from :func:`source_provenance`.

    Returns:
        False when the value is a refusal marker or carries a truncation marker,
        True otherwise. A value that was not read whole is not evidence about
        what produced the asset, so authentication treats it as absent rather
        than as a string to search.
    """
    return not (value.startswith(PROVENANCE_UNREAD_PREFIX)
                or PROVENANCE_TRUNCATED_PREFIX in value)


def conversion_version(value):
    """Return the converter version a provenance value names, or None.

    Args:
        value: one asset's ``general/source_script``, as read.

    Returns:
        The version string when the whole value is the measured conversion
        statement, ignoring surrounding whitespace and capitalisation, and None
        otherwise. Returning None for anything else is what makes a *negated*
        occurrence of the toolchain's name a failure rather than a pass: the
        name appears in "NOT created using NeuroConv" too, and a search cannot
        tell the two apart.
    """
    match = CONVERSION_SOURCE_FORM.match(value.strip().lower())
    return match.group("version") if match else None


def reference_instant(value):
    """Return the timezone-aware instant a reference-time value denotes, or None.

    Args:
        value: one asset's :data:`REFERENCE_TIME_PATH`, as read.

    Returns:
        A :class:`datetime.datetime` carrying a UTC offset when the whole value
        is an ISO-8601 timestamp that names one, ignoring surrounding
        whitespace; None otherwise.

    Note:
        **The shape is gated before the value is parsed, RC-004-F1.**
        :meth:`datetime.datetime.fromisoformat` accepts any single character
        where ISO-8601 puts ``T``, so ``2021-05-10Q14:33:49.023776-04:00``
        parsed, carried an offset, agreed with its pair and reached a drift
        verdict. :data:`REFERENCE_TIME_FORM` bounds the shape first; the
        parser still validates the values inside it, and the two are
        different jobs rather than one done twice.

        **A value without an offset is refused rather than assumed local.** An
        instant is a point in time; a wall-clock reading without an offset is
        not one, and choosing an offset for it -- UTC, or the machine's -- would
        invent the very quantity the comparison is about. All 142 assets
        measured in Session 33 carry an offset, so refusing is not refusing
        something this dandiset contains.

        **The comparison's resolution is one microsecond, and that is a
        property of the parser rather than a choice made here.**
        :meth:`datetime.datetime.fromisoformat` truncates fractional seconds
        below a microsecond, so two values differing only in their nanosecond
        digits parse equal and this check would call them the same instant. The
        measured disagreement in this dandiset is 3,600 s, nine orders of
        magnitude above that, so the resolution is stated rather than defended.
    """
    if not isinstance(value, str):
        return None
    text = value.strip()
    if REFERENCE_TIME_FORM.match(text) is None:
        return None
    try:
        parsed = datetime.datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed if parsed.utcoffset() is not None else None


def instant_text(instant):
    """Render an instant canonically, in UTC, for a record or a report.

    Args:
        instant: a timezone-aware :class:`datetime.datetime`.

    Returns:
        Its ISO-8601 form normalized to UTC, so two records of the same instant
        written at different declared offsets read as the same string. The
        declared value is recorded verbatim beside it and is not replaced by
        this one.
    """
    return instant.astimezone(datetime.timezone.utc).isoformat()


def authenticate_provenance(provenance, source):
    """Confirm one asset states its conversion and the origin of its times.

    The selection document pins the session-time origin to a conversion
    repository at a named commit and says in terms that an asset whose
    conversion provenance and values do not establish that common clock is an
    input error to resolve rather than a drift rejection. Recording the
    provenance is not that confirmation: a file carrying none at all was
    reaching a drift verdict with an empty provenance record, which is a
    malformed input becoming a verdict.

    Args:
        provenance: the dict :func:`source_provenance` returned.
        source: how to name the asset in the error, e.g. ``"raw asset X"``.

    Returns:
        A dict with ``path``, ``value``, ``version``, ``form``, ``token``,
        ``version_is_measured``, ``source``, ``reference_path``,
        ``reference_value`` and ``reference_instant`` -- the last a
        :class:`datetime.datetime`, which is why :func:`provenance_record` and
        not this dict is what a JSON record carries.

    Raises:
        ValueError: if either required path is absent, was not read whole, is
            not the measured conversion statement, or does not parse as a
            timezone-aware instant. All of them are input errors: they say the
            asset is not the one the clock claim is about, not that the
            candidate drifted.

    Note:
        **The conversion statement is checked before the reference time**, so a
        file that is not from the documented toolchain at all is refused on that
        rather than on a downstream property of a file this project is not
        reading anyway. The order is load-bearing for the error a reader sees,
        not for what is admitted.

        **A token search is not authentication, which is the repair here.** The
        first version required the case-insensitive substring ``neuroconv``
        anywhere in the value, and a value reading ``This asset was NOT created
        using NeuroConv; exported by LocalTool v3`` satisfied it: the search
        answered yes to a file that says no. The whole value is now matched
        against :data:`CONVERSION_SOURCE_FORM`, which is the exact sentence all
        21 assets measured in Session 7 carry, so what is authenticated is a
        positive statement rather than the presence of a word inside an
        arbitrary one. The version the sentence names is captured and reported;
        it is not matched against :data:`MEASURED_CONVERSION_VERSIONS`, for the
        reason recorded there.

        **The reference time is authenticated per asset rather than only across
        the pair**, so a value that is missing, refused, truncated, malformed or
        timezone-naive is an input error naming *which* asset is at fault. The
        alternative -- discovering it inside :func:`authenticate_provenance_pair`
        -- would report a defect in one file as a disagreement between two, and
        would let a raw asset's malformed value survive until the processed
        asset had already been opened.
    """
    value = provenance.get(REQUIRED_PROVENANCE_PATH)
    if value is None:
        raise ValueError(
            "%s carries no %s, so nothing in it states what produced it; the session-time "
            "origin this project reads from it is a property of the converter, and an asset "
            "that does not name one cannot establish it"
            % (source, REQUIRED_PROVENANCE_PATH))
    if not provenance_is_complete(value):
        raise ValueError(
            "%s carries a %s that was not read whole under the %d-byte provenance budget "
            "(%s), and a value this command did not fully see is not evidence about what "
            "produced the asset"
            % (source, REQUIRED_PROVENANCE_PATH, PROVENANCE_MAX_BYTES, ascii_safe(value)))
    version = conversion_version(value)
    if version is None:
        raise ValueError(
            "%s states %r as its %s, which is not the conversion statement %r that every "
            "one of the 21 assets of this dandiset measured in Session 7 carries. The "
            "whole value is matched rather than searched for %r, because a value that "
            "denies the toolchain contains its name too, so an asset outside the "
            "conversion path the session clock is pinned to is not admitted by naming it"
            % (source, ascii_safe(value), REQUIRED_PROVENANCE_PATH,
               CONVERSION_SOURCE_FORM_TEXT, CONVERSION_SOURCE_TOKEN))
    reference_value = provenance.get(REFERENCE_TIME_PATH)
    if reference_value is None:
        raise ValueError(
            "%s carries no %s, so nothing in it states the instant its time values are "
            "counted from; NWB defines every stored time as seconds relative to that "
            "instant, and an asset that does not name one cannot be placed on a shared "
            "session-time coordinate" % (source, REFERENCE_TIME_PATH))
    if not provenance_is_complete(reference_value):
        raise ValueError(
            "%s carries a %s that was not read whole under the %d-byte provenance budget "
            "(%s), and a value this command did not fully see is not evidence about where "
            "the asset's times begin"
            % (source, REFERENCE_TIME_PATH, PROVENANCE_MAX_BYTES,
               ascii_safe(reference_value)))
    instant = reference_instant(reference_value)
    if instant is None:
        raise ValueError(
            "%s states %r as its %s, which is not an ISO-8601 timestamp naming a UTC "
            "offset. The value must take the form %r before it is parsed at all, because "
            "the parser accepts any character where ISO-8601 puts the T; and a wall-clock "
            "reading with no offset is not an instant, so choosing one for it would invent "
            "the quantity the two assets are compared on. All 142 assets measured across "
            "71 sessions of this dandiset satisfy both"
            % (source, ascii_safe(reference_value), REFERENCE_TIME_PATH,
               REFERENCE_TIME_FORM_TEXT))
    return {"path": REQUIRED_PROVENANCE_PATH, "value": value, "version": version,
            "form": CONVERSION_SOURCE_FORM_TEXT, "token": CONVERSION_SOURCE_TOKEN,
            "version_is_measured": version in MEASURED_CONVERSION_VERSIONS,
            "source": source, "reference_path": REFERENCE_TIME_PATH,
            "reference_value": reference_value, "reference_instant": instant}


def provenance_record(authentication):
    """Return the JSON-safe half of an :func:`authenticate_provenance` result.

    Args:
        authentication: one asset's authentication result.

    Returns:
        A dict of strings and booleans: everything the record and the report
        need, with the parsed instant rendered canonically in UTC by
        :func:`instant_text` rather than carried as a
        :class:`datetime.datetime`.

    Note:
        This exists so the caller does not restate the key list once per asset.
        It did, and the two lists were identical -- which is the shape a later
        edit updates on one side only.
    """
    record = {key: authentication[key] for key in
              ("path", "token", "form", "version", "version_is_measured", "source",
               "reference_path", "reference_value")}
    record["reference_instant_utc"] = instant_text(authentication["reference_instant"])
    return record


def authenticate_provenance_pair(first, second):
    """Confirm two assets of one session count their times from the same instant.

    Authenticating each asset separately establishes that each came off the
    documented toolchain and that each states where its times begin. It does not
    establish that the two halves are on *one* coordinate, and the clock claim
    is about exactly that: the raw asset supplies the grid's extent while the
    processed asset supplies the spikes, so a drift number is only meaningful if
    both are counted from the same origin.

    **What is compared, and why it is not the converter version any more.** The
    condition here used to be equality of the parsed NeuroConv version. That
    version is a property of a library the conversion repository depends on, not
    of the session-time convention, and Session 33 measured what it admits: on
    71 sessions of DANDI 000409 -- 11 from the pinned candidate order and a
    60-session holdout drawn from the other 448, excluding the sessions the
    hypothesis came from -- the raw half was always 0.9.1 or 0.9.2 and the
    processed half always 0.9.4. **Agreement was 0 of 71: no candidate in this
    dandiset could ever have passed it.** On the same 71 sessions the declared
    reference instants agree on 63 and differ by exactly 3,600 s on 8, and the 8
    carry the same version pair as the 63 -- so the proxy was simultaneously too
    strict to admit anything and blind to the defect it stood in for. The
    versions are still parsed, still reported, and no longer decide anything.

    **What agreement here is worth, stated so the report cannot overstate it.**
    It is a *necessary declared* condition, not an identification of the clock.
    Two assets can declare the same origin and still have been written under
    different internal conventions; section 16.4 of the selection document
    already says containment cannot identify a clock either, and this cannot
    stand in for the converter semantics that argument rests on.

    **The strict branch is still the one taken, and the failure mode is still
    the recoverable one.** Nothing this project has measured says a one-hour
    disagreement is harmless, so a disagreement stops the run rather than being
    admitted with a justification the evidence does not support. Section 16.4
    makes that an input error, which **pauses** the pinned order rather than
    rejecting the candidate: the four candidates the measurement puts on the
    wrong side of this keep their rank, and recovering them needs its own
    evidence and its own recorded rule.

    Args:
        first: an :func:`authenticate_provenance` result, normally the raw one.
        second: the other asset's result.

    Returns:
        A dict with ``reference_instant_utc``, ``reference_instants_agree``
        (necessarily True, because the run stops otherwise),
        ``reference_delta_s``, both assets' ``raw_version`` and
        ``processed_version``, ``versions_agree`` -- which is **reported and
        does not gate**, and which is False on every real session of this
        dandiset -- and ``versions_are_measured``.

    Raises:
        ValueError: if the two declared instants differ. It is an input error
            about the asset pair, not a drift verdict.
    """
    if first["reference_instant"] != second["reference_instant"]:
        delta_s = (second["reference_instant"] - first["reference_instant"]).total_seconds()
        raise ValueError(
            "%s counts its times from %s and %s counts its times from %s, a difference of "
            "%+.6f s. NWB defines every time value in a file as seconds relative to that "
            "instant, so two assets naming different instants are not stating one "
            "session-time coordinate -- and the raw asset supplies the grid's extent while "
            "the processed asset supplies the spikes. Across 71 sessions of this dandiset "
            "the two halves agree exactly on 63 and differ by exactly +3600 s on 8, and "
            "nothing this command has measured says the difference is harmless. Resolve it "
            "as an input error, which pauses the pinned order rather than rejecting the "
            "candidate"
            % (first["source"], ascii_safe(first["reference_value"]),
               second["source"], ascii_safe(second["reference_value"]), delta_s))
    return {"reference_instant_utc": instant_text(first["reference_instant"]),
            "reference_instants_agree": True,
            "reference_delta_s": 0.0,
            "raw_version": first["version"],
            "processed_version": second["version"],
            # Reported, never gated. It is False on every session of DANDI
            # 000409 measured so far, which is exactly why it does not gate.
            "versions_agree": first["version"] == second["version"],
            "versions_are_measured": (first["version"] in MEASURED_CONVERSION_VERSIONS
                                      and second["version"] in MEASURED_CONVERSION_VERSIONS)}


@contextlib.contextmanager
def _ceiling_budget(reader, max_bytes):
    """Hold the caller's declared ceiling open as a transfer budget, or nothing.

    **Why the ceiling belongs here and not only after the plan.** The ceiling
    used to be checked once, against a plan written after preflight had already
    read the electrode table, the unit scalars, the descriptions and the
    provenance. On a fixture whose metadata is scattered across a 2 MB file at a
    1 MiB block, that is 2,081,456 distinct bytes spent before a one-byte
    ceiling refuses anything -- the refusal was correct and it was late. Held
    open around the whole read, the same number refuses before the first fetch.

    **In :func:`read_band_units` it cannot make anything infeasible, and that is
    the argument that licenses it there.** ``peak_resident_bytes`` contains
    ``cache_bound_bytes``, which is an upper bound on the distinct bytes the
    read fetches, so any read the plan check admits has already transferred no
    more than ``max_bytes``. Refusing a fetch that would cross ``max_bytes``
    therefore refuses only reads the later check would have refused anyway --
    earlier, and before the bytes move.

    **That argument does not carry to :func:`read_provenance`, and RC-004-F2 is
    where it stopped carrying.** There is no plan behind that read and so no
    later check to be redundant with, which makes the ceiling there a genuine
    tightening: a declared ceiling smaller than the cost of opening the raw
    asset now refuses a run that used to reach the processed read. That is the
    class a declared ceiling exists to refuse rather than a cost this function
    hides, it surfaces as an input error naming the ceiling, and at the
    command's 1024 MiB default it cannot fire. Stated here because the sentence
    above was written when :func:`read_band_units` was the only caller, and a
    universal claim that acquires a second caller is a claim about it too.

    Args:
        reader: the :class:`BoundedReader` the file is opened on.
        max_bytes: the declared ceiling, or None for no ceiling at all.

    Yields:
        None.
    """
    if max_bytes is None:
        yield
        return
    with reader.budget(None, int(max_bytes), label=PREFLIGHT_SCOPE):
        yield


def read_provenance(url, size, block_bytes, max_bytes=None):
    """Read one asset's conversion provenance and nothing else.

    The processed asset's provenance is read inside :func:`read_band_units`,
    where it is part of that read's plan. The raw asset supplies the clock's
    endpoints and its own electrode table, so its provenance has to be
    authenticated too, and this is the read that fetches it.

    Args:
        url: direct S3 URL of the NWB blob.
        size: the blob's size in bytes.
        block_bytes: range-request block size.
        max_bytes: the caller's declared ceiling, held open as a transfer
            budget around the whole call -- the file's superblock included --
            or None for no ceiling. **RC-004-F2 is what put it here.** The
            reference time this read fetches is half of the pair condition, and
            it was moving 23,920 distinct bytes of the raw asset before a
            declared ceiling of one byte refused the processed side. A budget
            the caller declared and a read that escapes it are the same defect
            class RC-003 closed one layer down.

    Returns:
        A dict with ``provenance``, ``provenance_io`` (both budgets and what
        each actually spent) and ``io`` (request count and bytes for the whole
        call, opening the file included). The provenance read itself is bounded
        before it happens rather than after it, and neither of its own two
        bounds grows with the recording's length or its spike count.

    Note:
        **This read is inside the caller's ceiling, and the ceiling is entered
        before the file is opened.** ``_ceiling_budget`` is held open around
        the open and the provenance read together, exactly as
        :func:`read_band_units` holds it, so a fetch that would cross the
        declared ceiling is refused before its bytes move rather than reported
        after them. **It is a tightening and it can refuse a run that used to
        reach a verdict** -- one whose declared ceiling is smaller than the cost
        of opening the raw asset and reading two short values. That is the
        class the ceiling exists to refuse, it is reported as an input error
        naming the ceiling, and at the command's 1024 MiB default it cannot
        fire.

        **The block size is capped here rather than taken from the caller.**
        This read has no *plan* behind it -- no band, no footprint to compare
        against -- so its own transfer bound is what stands between a malformed
        asset and an unbounded spend inside whatever ceiling the caller
        declared. A bound denominated in blocks cannot be smaller than a block,
        so a 1 MiB block
        chosen for a bulk payload read on a *different* file would make this
        read's bound 5,308,416 bytes for the sake of about eighty characters
        across two required paths. At :data:`PROVENANCE_BLOCK_BYTES` it is
        393,216.
    """
    remote = RemoteFile(url, size, block=min(int(block_bytes), PROVENANCE_BLOCK_BYTES))
    reader = BoundedReader(remote)
    # The ceiling is entered before the file is opened, so it covers every byte
    # this call fetches. last_spend is read inside it, while the provenance
    # scope is still the most recently closed one -- reading it after the
    # ceiling scope exits would report the ceiling's spend under the
    # provenance label.
    with _ceiling_budget(reader, max_bytes), h5py.File(reader, "r") as handle:
        provenance = source_provenance(handle, reader)
        spend = reader.last_spend
    return {"provenance": provenance,
            "provenance_io": spend,
            "io": {"requests": remote.n_requests, "bytes": remote.n_bytes}}


def read_integer_column(node, name, require_integer_dtype=False):
    """Read a units-table column that must be integral as it is stored.

    A ragged partition offset and an electrode row reference are both indices
    into something else, so a value that is not a whole number is not a small
    inaccuracy -- it is a structural claim the file cannot support. ``int()``
    would accept it and truncate: two offsets 0.75 apart become one partition,
    and a fractional electrode becomes a real row. The check therefore runs on
    the stored values, before any conversion.

    ``require_integer_dtype`` is the stricter rule the ragged indices are held
    to. They are HDMF ``VectorIndex`` datasets and the common schema specifies
    unsigned-integer storage, so a floating-point index is a malformed file and
    exact whole values do not repair it. The custom ``max_electrode`` column
    carries no such specification, so it is read with the flag off: whole-valued
    floats are accepted there and the stored dtype is reported.

    Args:
        node: the open units-table group.
        name: the column name.
        require_integer_dtype: reject a non-integer storage dtype outright,
            for columns whose schema requires integer storage.

    Returns:
        The column as a list of Python ints.

    Raises:
        ValueError: if the column is not stored in an integer dtype and either
            ``require_integer_dtype`` is set or its values are not all finite
            whole numbers.
    """
    values = node[name][:]
    if np.issubdtype(values.dtype, np.integer):
        return [int(v) for v in values]
    if require_integer_dtype:
        raise ValueError(
            "units column %r is stored as %s, but it is an HDMF VectorIndex and the "
            "common schema specifies integer storage for it; a floating-point ragged "
            "index is a malformed file rather than an encoding choice, and values that "
            "happen to be whole do not make it well formed" % (name, values.dtype))
    if not np.issubdtype(values.dtype, np.floating):
        raise ValueError(
            "units column %r has dtype %s, which is neither integer nor float; it is "
            "used as an index and must be whole numbers" % (name, values.dtype))
    if not np.all(np.isfinite(values)):
        raise ValueError(
            "units column %r holds %d non-finite values and is used as an index"
            % (name, int((~np.isfinite(values)).sum())))
    fractional = values != np.floor(values)
    if np.any(fractional):
        first = int(np.argmax(fractional))
        raise ValueError(
            "units column %r is stored as %s and its value at row %d is %r, which is not a "
            "whole number; it indexes another table and truncating it would invent a "
            "structure the file does not state" % (name, values.dtype, first, values[first]))
    return [int(v) for v in values]


def read_unit_scalars(handle):
    """Read the one-value-per-unit columns the band selection needs.

    Args:
        handle: an open :class:`h5py.File`.

    Returns:
        A dict with ``probe_name`` and ``label`` (lists of str),
        ``max_electrode`` (list of int), ``times_index`` and ``depths_index``
        (lists of int, the ragged columns' own end-offset indices),
        ``n_units``, ``n_times`` / ``n_depths``, the two ragged columns' total
        lengths, and ``integer_dtypes``, each structural column's stored dtype
        as a string, so the report can say what was checked rather than that a
        check was made.

    Raises:
        KeyError: if the units table or either ragged column is absent.
        ValueError: if either ragged index is not stored in an integer dtype, if
            a structural column is not integral as stored, or if any
            one-value-per-unit column does not hold exactly one value per unit.
            A short column would otherwise silently shorten the unit set.
    """
    if UNITS_PATH not in handle:
        raise KeyError("file has no /%s" % UNITS_PATH)
    node = handle[UNITS_PATH]
    for name in (TIME_COLUMN, DEPTH_COLUMN,
                 TIME_COLUMN + "_index", DEPTH_COLUMN + "_index", "probe_name",
                 "max_electrode"):
        if name not in node:
            raise KeyError("units table has no %s" % name)
    probe_name = _decode(node["probe_name"][:])
    n_units = len(probe_name)
    scalars = {
        "probe_name": probe_name,
        "label": (_decode(node["kilosort2_label"][:])
                  if "kilosort2_label" in node else [""] * n_units),
        "max_electrode": read_integer_column(node, "max_electrode"),
        "times_index": read_integer_column(node, TIME_COLUMN + "_index",
                                           require_integer_dtype=True),
        "depths_index": read_integer_column(node, DEPTH_COLUMN + "_index",
                                            require_integer_dtype=True),
        "n_units": n_units,
        "n_times": int(node[TIME_COLUMN].shape[0]),
        "n_depths": int(node[DEPTH_COLUMN].shape[0]),
        "integer_dtypes": {name: str(node[name].dtype) for name in
                           ("max_electrode", TIME_COLUMN + "_index",
                            DEPTH_COLUMN + "_index")},
    }
    for name in ("label", "max_electrode", "times_index", "depths_index"):
        if len(scalars[name]) != n_units:
            raise ValueError(
                "the units table holds %d probe_name values but %d %s values; every "
                "one-value-per-unit column must have one value per unit"
                % (n_units, len(scalars[name]), name))
    return scalars


def check_ragged_alignment(scalars):
    """Confirm the two ragged columns partition their spikes identically.

    The drift statistic pairs each spike's time with that spike's depth, so the
    two columns must not merely have the same total length -- they must cut it
    into the same per-unit slices, in the same order. NWB stores each ragged
    column's end offsets in its own ``_index`` dataset, and nothing in the
    format requires two such columns to agree. This checks that they do.

    Args:
        scalars: the dict returned by :func:`read_unit_scalars`.

    Raises:
        ValueError: if either index is not non-decreasing, if either fails to
            end at its column's length, or if the two indices differ anywhere.
            Each is an input error rather than an unmeasurable candidate.
    """
    times_index = scalars["times_index"]
    depths_index = scalars["depths_index"]
    n_units = scalars["n_units"]
    for name, index, total in (("%s_index" % TIME_COLUMN, times_index, scalars["n_times"]),
                               ("%s_index" % DEPTH_COLUMN, depths_index, scalars["n_depths"])):
        if len(index) != n_units:
            raise ValueError(
                "%s has %d entries for %d units" % (name, len(index), n_units))
        if any(index[i] > index[i + 1] for i in range(len(index) - 1)):
            raise ValueError("%s is not non-decreasing" % name)
        if index and index[0] < 0:
            raise ValueError("%s starts at a negative offset %d" % (name, index[0]))
        if index and index[-1] != total:
            raise ValueError(
                "%s ends at %d but the column holds %d values" % (name, index[-1], total))
    if times_index != depths_index:
        first = next(i for i in range(n_units) if times_index[i] != depths_index[i])
        raise ValueError(
            "the %s and %s ragged indices first disagree at unit %d (%d vs %d); a unit's "
            "times and depths would not be the same spikes"
            % (TIME_COLUMN, DEPTH_COLUMN, first, times_index[first], depths_index[first]))


def resolve_unit_electrodes(scalars, electrodes, probe):
    """Map each unit on one probe to a finite ``rel_y`` on that same probe.

    Args:
        scalars: the dict returned by :func:`read_unit_scalars`.
        electrodes: the dict returned by :func:`read_flat_electrodes`, from the
            **same** file, so that ``max_electrode`` indexes the table the
            depths are taken from.
        probe: the probe name to restrict to, exactly as stored.

    Returns:
        A list of dicts, one per unit on ``probe``, each with ``row`` (units
        table row index), ``probe``, ``max_electrode``, ``rel_y_um`` and
        ``label``.

    Raises:
        ValueError: if a unit's ``max_electrode`` is out of range, belongs to a
            different probe, or resolves to a non-finite ``rel_y``. Band
            membership is decided by this mapping, so an ambiguous mapping is an
            input error and never permission to translate the band.
    """
    rows = []
    for row, unit_probe in enumerate(scalars["probe_name"]):
        if unit_probe != probe:
            continue
        electrode = scalars["max_electrode"][row]
        if not 0 <= electrode < electrodes["n_rows"]:
            raise ValueError(
                "unit %d on probe %r has max_electrode %d, outside an electrode table of "
                "%d rows" % (row, probe, electrode, electrodes["n_rows"]))
        owner = electrodes["group_name"][electrode]
        if owner != unit_probe:
            raise ValueError(
                "unit %d says probe %r but its max_electrode %d belongs to probe %r"
                % (row, unit_probe, electrode, owner))
        rel_y = electrodes["rel_y"][electrode]
        if not np.isfinite(rel_y):
            raise ValueError(
                "unit %d resolves to electrode %d whose rel_y is %r, not a finite depth"
                % (row, electrode, rel_y))
        rows.append({
            "row": row,
            "probe": unit_probe,
            "max_electrode": electrode,
            "rel_y_um": float(rel_y),
            "label": scalars["label"][row],
        })
    return rows


def select_band_units(unit_electrodes, depth_lo_um, depth_hi_um):
    """Keep the units whose peak electrode sits inside the pinned band.

    Args:
        unit_electrodes: the list returned by :func:`resolve_unit_electrodes`.
        depth_lo_um: the band's lower ``rel_y`` bound, inclusive.
        depth_hi_um: the band's upper ``rel_y`` bound, inclusive.

    Returns:
        The subset of ``unit_electrodes`` inside the band, in units-table row
        order. The selection reads no quality label: every unit whose peak
        electrode lands in the band contributes, which is the pre-declared
        label-blind rule.
    """
    return [unit for unit in unit_electrodes
            if depth_lo_um <= unit["rel_y_um"] <= depth_hi_um]


def chunk_byte_ranges(dataset, slices):
    """Locate in the file every chunk a set of element slices touches.

    An HDF5 chunk is stored contiguously, but successive chunks of one dataset
    are not: the library allocates each chunk where it can, so a file written
    incrementally, or alongside other growing datasets, interleaves them with
    unrelated data. Treating the first-to-last chunk span as one contiguous
    region therefore under-counts the blocks a fixed-block reader touches, by
    however much other data sits between them. The chunk index knows where each
    one is, so this asks it rather than assuming.

    Args:
        dataset: an open chunked :class:`h5py.Dataset`.
        slices: ``(lo, hi)`` element ranges, half-open.

    Returns:
        A dict from a chunk's first element to its ``(byte_offset, size)``, with
        None for a chunk the file has not allocated (an unwritten chunk costs no
        transfer). None if the dataset is not chunked or the chunk index will
        not answer, which the caller must treat as an unknown layout rather than
        as an empty one.
    """
    chunks = dataset.chunks
    if not chunks:
        return None
    chunk = int(chunks[0])
    wanted = set()
    for lo, hi in slices:
        if hi <= lo:
            continue
        for start in range((lo // chunk) * chunk, hi, chunk):
            wanted.add(start)
    ranges = {}
    for start in sorted(wanted):
        try:
            info = dataset.id.get_chunk_info_by_coord((start,))
        except (AttributeError, TypeError, ValueError, OSError, RuntimeError):
            return None
        if info is None or getattr(info, "byte_offset", None) is None:
            ranges[start] = None
            continue
        ranges[start] = (int(info.byte_offset), int(info.size))
    return ranges


def column_layout(dataset, slices=None):
    """Describe one stored column's layout, as the file itself reports it.

    Args:
        dataset: an open :class:`h5py.Dataset`.
        slices: the ``(lo, hi)`` element ranges the read will take. When given
            and the dataset is chunked, the chunk index is consulted so the
            plan can place every touched chunk exactly. Reading the index costs
            range requests, so the caller does this before it records what the
            read has already spent.

    Returns:
        A dict with ``itemsize``, ``offset`` (the dataset's byte offset in the
        file when it is stored contiguously, else None), ``chunk_elements``
        (the first chunk dimension when the dataset is chunked, else None),
        ``chunk_map`` (from :func:`chunk_byte_ranges`, else None),
        ``storage_bytes`` (what the file spends on it), ``library_cache_bytes``
        (the size HDF5's own raw-data chunk cache is allowed to reach for this
        dataset, which is memory the read occupies without ever appearing in a
        Python object) and ``compression``.
    """
    try:
        offset = dataset.id.get_offset()
    except (AttributeError, TypeError, ValueError):
        offset = None
    chunks = dataset.chunks
    try:
        storage_bytes = int(dataset.id.get_storage_size())
    except (AttributeError, TypeError, ValueError):
        storage_bytes = None
    library_cache_bytes = 0
    if chunks:
        try:
            library_cache_bytes = int(dataset.id.get_access_plist().get_chunk_cache()[1])
        except (AttributeError, TypeError, ValueError, OSError, RuntimeError):
            # Unreadable rather than absent: charge the library's documented
            # default rather than nothing, because nothing would be a claim.
            library_cache_bytes = 1024 * 1024
    return {
        "itemsize": int(dataset.dtype.itemsize),
        "offset": None if offset is None else int(offset),
        "chunk_elements": int(chunks[0]) if chunks else None,
        "chunk_map": (chunk_byte_ranges(dataset, slices)
                      if slices is not None and chunks else None),
        "storage_bytes": storage_bytes,
        "library_cache_bytes": library_cache_bytes,
        "compression": dataset.compression,
    }


def _blocks_covering(start, length, block_bytes):
    """Return the block indices a byte range occupies."""
    if length <= 0:
        return set()
    return set(range(start // block_bytes,
                     (start + length - 1) // block_bytes + 1))


def _slice_blocks(lo, hi, layout, block_bytes):
    """Name the distinct blocks one column slice can cost, and how it was placed.

    A block-caching reader fetches whole fixed-width blocks, so the cost of a
    slice is the blocks it lands in rather than its own length. Three regimes,
    in decreasing order of what the file will tell us:

    * **a chunked dataset whose chunk index answered** -- every chunk the slice
      touches is placed at its own file byte range, and the blocks covering
      those ranges are returned. A chunked read fetches whole chunks, so a
      partially used chunk still costs all of its blocks;
    * **contiguous storage with a known file offset** -- the slice's byte range
      is known directly;
    * **neither** -- nothing is known about where the bytes are, so no block set
      can be named and the caller must fall back to the whole file.

    Args:
        lo: first element of the slice.
        hi: one past the last element.
        layout: the dict from :func:`column_layout`.
        block_bytes: the reader's block size.

    Returns:
        A ``(blocks, basis)`` pair. ``blocks`` is a set of block indices, or
        None when the layout is unknown; ``basis`` names how it was derived.
    """
    if hi <= lo:
        return set(), None
    chunk_map = layout.get("chunk_map")
    chunk = layout["chunk_elements"]
    if chunk_map is not None and chunk:
        blocks = set()
        for start in range((lo // chunk) * chunk, hi, chunk):
            if start not in chunk_map:
                return None, "whole file"
            located = chunk_map[start]
            if located is None:
                continue
            blocks |= _blocks_covering(located[0], located[1], block_bytes)
        return blocks, "chunk offsets"
    if layout["offset"] is not None and not chunk:
        start = layout["offset"] + lo * layout["itemsize"]
        return (_blocks_covering(start, (hi - lo) * layout["itemsize"], block_bytes),
                "dataset offsets")
    return None, "whole file"


def python_structure_bytes(*objects):
    """Measure the live Python containers a read holds, conservatively.

    The block cache and the converted arrays are the two large terms in what
    this read occupies, but they are not the only ones: the unit scalars, the
    electrode table and the per-unit records are lists and dicts of Python
    objects that stay alive for the whole read. This walks them with
    :func:`sys.getsizeof` and counts a shared object once per reference, which
    over-counts rather than under-counts.

    Args:
        *objects: the containers to charge for.

    Returns:
        The total in bytes.
    """

    def walk(obj, depth):
        total = sys.getsizeof(obj)
        if depth >= 6:
            return total
        if isinstance(obj, dict):
            for key, value in obj.items():
                total += walk(key, depth + 1) + walk(value, depth + 1)
        elif isinstance(obj, (list, tuple, set, frozenset)):
            for item in obj:
                total += walk(item, depth + 1)
        return total

    return sum(walk(obj, 0) for obj in objects)


def band_slices(band_units, index):
    """Return each band unit's ``(lo, hi)`` element range in the ragged columns."""
    return [_slice_bounds(index, unit["row"]) for unit in band_units]


def plan_transfer(band_units, scalars, time_layout, depth_layout,
                  block_bytes, file_size, spent_bytes=0, held=()):
    """Size the band units' read before any of it is spent.

    The numbers answer different questions and the project's compute rule needs
    all of them: what the slices hold, what the network fetch can cost, and what
    has to fit in memory at once. Reporting one of them as ``bytes`` is what let
    a ceiling pass a read that then transferred more than the ceiling allowed;
    reporting the memory ones separately is what let a ceiling pass a read whose
    parts each fit but which together did not.

    Args:
        band_units: the list returned by :func:`select_band_units`.
        scalars: the dict returned by :func:`read_unit_scalars`.
        time_layout: :func:`column_layout` for the spike-time column.
        depth_layout: :func:`column_layout` for the spike-depth column.
        block_bytes: the reader's block size, which is what actually gets
            fetched.
        file_size: the asset's total size, which caps distinct block bytes.
        spent_bytes: bytes already transferred resolving the index and the
            metadata. Already spent, and part of what this read costs.
        held: any further live containers the caller holds for the duration of
            the read -- the electrode table and the per-unit records -- charged
            into ``structures_bytes``.

    Returns:
        A dict with ``n_units``, ``n_spikes``, ``per_unit`` (``(row, n_spikes)``
        pairs), ``logical_bytes`` (exact stored payload), ``cache_bound_bytes``
        (an upper bound on distinct block bytes, ``spent_bytes`` included),
        ``resident_bytes`` (the converted arrays plus the largest slice at its
        stored width), ``structures_bytes`` (the live Python containers),
        ``library_cache_bytes`` (what HDF5's own raw-data chunk cache is allowed
        to reach for the two columns), ``peak_resident_bytes`` (the sum of the
        previous four), ``bound_basis`` naming how the block bound was derived,
        plus ``block_bytes``, ``spent_bytes`` and the two layouts.

    Note:
        ``cache_bound_bytes`` bounds *distinct* blocks. A range request that
        fails and is retried re-transfers its block, and that is deliberately
        outside this bound: it is a network condition rather than a property of
        the read being planned.

        ``peak_resident_bytes`` adds the memory terms because they are live at
        the same moment, not one after another: the reader's block cache is
        unbounded and is not released until the read returns, so the last unit's
        arrays are resident while every block that fed the first unit is still
        resident too. Its declared scope is the block cache, the converted
        per-unit arrays with the largest stored-width slice, the Python
        containers this call is given, and the ceiling HDF5's own raw-data chunk
        cache is allowed to reach for the two columns. What it does **not**
        cover is named rather than left to be discovered: the interpreter's
        baseline, the allocator's fragmentation overhead, and any transient
        h5py allocation outside a chunk cache. It bounds this read's own
        footprint, not the process's.
    """
    index = scalars["times_index"]
    per_unit = []
    total_spikes = 0
    largest = 0
    slices = []
    for unit in band_units:
        lo, hi = _slice_bounds(index, unit["row"])
        per_unit.append((unit["row"], hi - lo))
        total_spikes += hi - lo
        largest = max(largest, hi - lo)
        slices.append((lo, hi))

    bounded_bytes = 0
    bases = []
    for layout in (time_layout, depth_layout):
        known_blocks = set()
        unknown = False
        for lo, hi in slices:
            blocks, basis = _slice_blocks(lo, hi, layout, block_bytes)
            if blocks is None:
                unknown = True
                break
            known_blocks |= blocks
            if basis is not None and basis not in bases:
                bases.append(basis)
        if unknown:
            # Nothing is known about where this column's bytes sit, so the only
            # remaining true statement is that the reader cannot fetch more
            # distinct bytes than the file holds.
            if "whole file" not in bases:
                bases.append("whole file")
            bounded_bytes += int(file_size)
            continue
        for block in known_blocks:
            bounded_bytes += min(block_bytes, max(0, file_size - block * block_bytes))
        # One block per column for the object-header and chunk-index metadata
        # h5py reads alongside the payload, which is not inside the payload's
        # own byte range and so is not in the block set above.
        bounded_bytes += block_bytes

    cache_bound = min(int(file_size), spent_bytes + bounded_bytes)
    resident = total_spikes * 16 + largest * (time_layout["itemsize"]
                                              + depth_layout["itemsize"])
    structures = python_structure_bytes(band_units, scalars, time_layout,
                                        depth_layout, *held)
    library_cache = (time_layout.get("library_cache_bytes", 0)
                     + depth_layout.get("library_cache_bytes", 0))
    return {
        "n_units": len(band_units),
        "n_spikes": total_spikes,
        "per_unit": per_unit,
        "logical_bytes": total_spikes * (time_layout["itemsize"]
                                         + depth_layout["itemsize"]),
        "cache_bound_bytes": cache_bound,
        "resident_bytes": resident,
        "structures_bytes": structures,
        "library_cache_bytes": library_cache,
        "peak_resident_bytes": cache_bound + resident + structures + library_cache,
        "bound_basis": (" + ".join(bases) if bases else "no slices"),
        "block_bytes": int(block_bytes),
        "spent_bytes": int(spent_bytes),
        "time_layout": time_layout,
        "depth_layout": depth_layout,
    }


def _slice_bounds(index, row):
    """Return the ``[lo, hi)`` bounds of one unit's ragged slice."""
    return (index[row - 1] if row > 0 else 0), index[row]


def read_band_units(url, size, block_bytes, probe, depth_lo_um, depth_hi_um,
                    max_bytes=None, plan_only=False, expect_conversion=None):
    """Read the pinned band's per-unit spike times and per-spike depths.

    Args:
        url: direct S3 URL of the **processed** NWB blob.
        size: the blob's size in bytes.
        block_bytes: HTTP range-request block size. Scattered ragged slices
            transfer far less at 1 MiB than at the module default.
        probe: the probe name to read, exactly as stored in ``probe_name``.
        depth_lo_um: the pinned band's lower ``rel_y`` bound, inclusive.
        depth_hi_um: the pinned band's upper ``rel_y`` bound, inclusive.
        max_bytes: refuse the read if ``peak_resident_bytes`` -- the block cache,
            the converted arrays and the live Python structures together --
            would exceed this many bytes. It is also held open as a transfer
            budget for the whole call, so a read that would push the distinct
            bytes fetched past it is refused *before* it fetches rather than
            reported afterwards; see :func:`_ceiling_budget` for why that cannot
            refuse anything the later check would have admitted. That single quantity is what a free-RAM
            measurement has to be compared against, and because it contains the
            block-transfer bound it also refuses everything a transfer-only
            ceiling would have refused. None means no ceiling, which is the
            caller taking responsibility for the whole footprint.
        plan_only: resolve and validate the index and the band membership, then
            return without reading any spike data.
        expect_conversion: the raw asset's :func:`authenticate_provenance`
            result, when the caller has one. Given it, this read also requires
            the two assets to declare the same session-time origin, and it does
            so in preflight -- before the plan, and before a single spike is
            read -- because a pair check run after the payload would cost the
            whole read to reject the asset.

    Returns:
        A dict carrying ``probe``, ``band`` (the two bounds), ``plan`` (from
        :func:`plan_transfer`), ``descriptions``, ``provenance``,
        ``provenance_io`` (the two provenance budgets and what each spent),
        ``electrodes``, ``unit_electrodes`` (every unit on the probe),
        ``band_units`` (the in-band subset, each with ``times`` and ``depths``
        arrays unless ``plan_only``), ``n_units_on_probe``,
        ``integer_dtypes`` (each structural column as stored) and ``io``
        (request count and bytes transferred, which includes metadata as well
        as spikes).

    Raises:
        KeyError: if the file lacks the units or electrodes table.
        ValueError: on any of the four input-error conditions this module
            checks, or if the planned peak resident footprint exceeds
            ``max_bytes``.
    """
    remote = RemoteFile(url, size, block=block_bytes)
    reader = BoundedReader(remote)
    # The ceiling is entered before the file is opened, so it covers every byte
    # this call fetches -- the superblock included -- rather than only the ones
    # spent after a plan exists to compare against.
    with _ceiling_budget(reader, max_bytes), h5py.File(reader, "r") as handle:
        electrodes = read_flat_electrodes(handle)
        scalars = read_unit_scalars(handle)
        check_ragged_alignment(scalars)
        descriptions = column_descriptions(handle)
        # Read here, in preflight, and never after the ceiling is enforced.
        # source_provenance reads complete stored datasets, so a call placed
        # after the check spends bytes the plan has already promised were
        # bounded -- which is exactly what it used to do. The budget is the
        # other half: preflight makes the spend accounted, the budget makes it
        # refusable, and a value that cannot be refused is not bounded merely
        # because someone counted it.
        provenance = source_provenance(handle, reader)
        provenance_io = reader.last_spend
        authentication = authenticate_provenance(
            provenance, "processed asset %s" % url.rsplit("/", 1)[-1])
        pair = (authenticate_provenance_pair(expect_conversion, authentication)
                if expect_conversion is not None else None)

        depth_description = descriptions.get(DEPTH_COLUMN)
        if not depth_description or DEPTH_UNIT_PHRASE not in depth_description.lower():
            raise ValueError(
                "the %s column's description does not state its unit as %r; it reads %r"
                % (DEPTH_COLUMN, DEPTH_UNIT_PHRASE, depth_description))

        unit_electrodes = resolve_unit_electrodes(scalars, electrodes, probe)
        if not unit_electrodes:
            raise ValueError(
                "no unit names probe %r; the file's probes are %s"
                % (probe, sorted(set(scalars["probe_name"]))))
        band_units = select_band_units(unit_electrodes, depth_lo_um, depth_hi_um)

        node = handle[UNITS_PATH]
        times_dataset = node[TIME_COLUMN]
        depths_dataset = node[DEPTH_COLUMN]
        # The layouts are resolved before spent_bytes is read, because placing a
        # chunked column costs range requests of its own and they are part of
        # what this read spends.
        slices = band_slices(band_units, scalars["times_index"])
        time_layout = column_layout(times_dataset, slices)
        depth_layout = column_layout(depths_dataset, slices)
        plan = plan_transfer(band_units, scalars, time_layout, depth_layout,
                             block_bytes, size, spent_bytes=remote.n_bytes,
                             held=(electrodes, unit_electrodes, descriptions,
                                   provenance))
        if max_bytes is not None and plan["peak_resident_bytes"] > max_bytes:
            raise ValueError(
                "reading %d band units (%d spikes, %d bytes of stored payload) would hold "
                "%d bytes at once -- %d bytes of retained block cache (%s), %d bytes of "
                "converted arrays, %d bytes of Python structures and %d bytes of HDF5 "
                "chunk cache, all live together -- and peak_resident_bytes is above the "
                "declared ceiling of %d. Raise the ceiling deliberately against a "
                "measurement of free memory, or read a smaller band."
                % (plan["n_units"], plan["n_spikes"], plan["logical_bytes"],
                   plan["peak_resident_bytes"], plan["cache_bound_bytes"],
                   plan["bound_basis"], plan["resident_bytes"],
                   plan["structures_bytes"], plan["library_cache_bytes"], max_bytes))

        result = {
            "probe": probe,
            "band": {"depth_lo_um": float(depth_lo_um), "depth_hi_um": float(depth_hi_um)},
            "plan": plan,
            "descriptions": descriptions,
            "provenance": provenance,
            "provenance_authentication": authentication,
            "provenance_pair": pair,
            "provenance_io": provenance_io,
            "electrodes": electrodes,
            "unit_electrodes": unit_electrodes,
            "band_units": band_units,
            "n_units_on_probe": len(unit_electrodes),
            "n_units_total": scalars["n_units"],
            "integer_dtypes": scalars["integer_dtypes"],
            "plan_only": bool(plan_only),
        }
        if plan_only:
            result["io"] = {"requests": remote.n_requests, "bytes": remote.n_bytes}
            return result

        for unit in band_units:
            lo, hi = _slice_bounds(scalars["times_index"], unit["row"])
            times = np.asarray(times_dataset[lo:hi], dtype=np.float64)
            depths = np.asarray(depths_dataset[lo:hi], dtype=np.float64)
            if times.size != depths.size:
                raise ValueError(
                    "unit %d read %d times and %d depths from the same slice [%d, %d)"
                    % (unit["row"], times.size, depths.size, lo, hi))
            if times.size and not np.all(np.isfinite(times)):
                raise ValueError(
                    "unit %d carries %d non-finite spike times"
                    % (unit["row"], int((~np.isfinite(times)).sum())))
            if depths.size and not np.all(np.isfinite(depths)):
                raise ValueError(
                    "unit %d carries %d non-finite spike depths"
                    % (unit["row"], int((~np.isfinite(depths)).sum())))
            if times.size > 1 and np.any(np.diff(times) < 0):
                raise ValueError(
                    "unit %d's spike times are not ascending; the binning assumes they are"
                    % unit["row"])
            unit["slice"] = [int(lo), int(hi)]
            unit["n_spikes"] = int(times.size)
            unit["times"] = times
            unit["depths"] = depths
        result["io"] = {"requests": remote.n_requests, "bytes": remote.n_bytes}
    return result


def electrode_tables_agree(raw_probe_rows, processed, probe):
    """Compare the raw and processed files' electrode tables for one probe.

    The band is derived from the raw file's table, while ``max_electrode``
    indexes the processed file's. If the two disagree, a band derived from one
    is being applied to units placed by the other.

    Args:
        raw_probe_rows: the raw file's per-electrode dicts for ``probe``, as
            ``utils.host_anatomy.read_electrode_table`` returns them.
        processed: the dict returned by :func:`read_flat_electrodes` on the
            processed file.
        probe: the probe name.

    Returns:
        A dict with ``agree`` and, when they do not, ``detail`` naming the first
        difference and the two row counts.
    """
    processed_rows = [(processed["rel_y"][i], processed["location"][i])
                      for i in range(processed["n_rows"])
                      if processed["group_name"][i] == probe]
    raw_rows = [(row["depth_um"], row["location"]) for row in raw_probe_rows]
    if len(raw_rows) != len(processed_rows):
        return {"agree": False,
                "detail": "raw table has %d rows for probe %s, processed has %d"
                          % (len(raw_rows), probe, len(processed_rows))}
    for index, (raw_row, processed_row) in enumerate(zip(raw_rows, processed_rows)):
        if raw_row != processed_row:
            return {"agree": False,
                    "detail": "row %d differs: raw %r, processed %r"
                              % (index, raw_row, processed_row)}
    return {"agree": True, "detail": "%d rows identical" % len(raw_rows)}
