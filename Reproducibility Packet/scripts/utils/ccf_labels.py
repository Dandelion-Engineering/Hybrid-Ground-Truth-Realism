"""Map Allen CCF long structure names to the acronyms the donor library uses.

Region matching in Tier A compares two vocabularies that describe the same
atlas but do not spell it the same way:

- the **host** side. DANDI 000409 NWB files annotate each electrode with the
  Allen CCF *long name* in ``/general/extracellular_ephys/electrodes/location``
  -- ``Field CA1``, ``Rostrolateral area layer 5``, ``fiber tracts``.
- the **donor** side. ``hybrid_template_library``'s ``brain_area`` column holds
  the Allen *acronym* -- ``CA1``, ``VISrl5``, ``CP``.

Without a bridge between them, "region-matched" cannot be evaluated at all.
This module is that bridge, restricted to the structures this project can
actually reach: every area holding at least ten in-caliper Neuropixels 1.0
templates, plus the neighbouring structures those probes pass through.

**This table is hand-authored and must be treated as a claim, not a fact.**
``validate_ccf_label_map.py`` checks it against the donor library's own
(session, depth, acronym) records, which is independent evidence from the data
rather than from whoever typed the table. Entries that the validator has not
confirmed stay in, but the validator reports them as unconfirmed, and callers
should surface unmapped host labels loudly rather than dropping them.

Matching is done on a normalised key, because the NWB export strips the commas
that appear in the canonical Allen names ("Dentate gyrus, molecular layer"
becomes "Dentate gyrus molecular layer").
"""

import json
import os
import re

_PUNCT_RE = re.compile(r"[,\.]")
_SPACE_RE = re.compile(r"\s+")

# Canonical Allen CCF long name -> template-library acronym.
# Ordered by the structure families the project's candidate hosts traverse.
NAME_TO_ACRONYM = {
    # Hippocampal formation
    "Field CA1": "CA1",
    "Field CA2": "CA2",
    "Field CA3": "CA3",
    "Dentate gyrus, molecular layer": "DG-mo",
    "Dentate gyrus, granule cell layer": "DG-sg",
    "Dentate gyrus, polymorph layer": "DG-po",
    "Subiculum": "SUB",
    "Prosubiculum": "ProS",
    "Postsubiculum": "POST",
    # Entorhinal cortex
    "Entorhinal area, lateral part, layer 3": "ENTl3",
    "Entorhinal area, lateral part, layer 5": "ENTl5",
    "Entorhinal area, lateral part, layer 6a": "ENTl6a",
    # Striatum, pallidum, amygdala
    "Caudoputamen": "CP",
    "Medial amygdalar nucleus": "MEA",
    "Basomedial amygdalar nucleus, posterior part": "BMAp",
    # Olfactory
    "Anterior olfactory nucleus": "AON",
    "Piriform area": "PIR",
    # Thalamus and midbrain
    "Lateral posterior nucleus of the thalamus": "LP",
    "Paraventricular nucleus of the thalamus": "PVT",
    "Midbrain reticular nucleus": "MRN",
    "Periaqueductal gray": "PAG",
    "Septofimbrial nucleus": "SF",
    # Visual and associated cortex
    "Anterior area, layer 2/3": "VISa2/3",
    "Anterior area, layer 5": "VISa5",
    "Rostrolateral area, layer 2/3": "VISrl2/3",
    "Rostrolateral area, layer 4": "VISrl4",
    "Rostrolateral area, layer 5": "VISrl5",
    "Rostrolateral area, layer 6a": "VISrl6a",
    "Postrhinal area, layer 5": "VISpor5",
    "Postrhinal area, layer 6a": "VISpor6a",
    "Laterointermediate area, layer 4": "VISli4",
    "Visceral area, layer 5": "VISC5",
    # Somatomotor and somatosensory cortex
    "Primary motor area, layer 5": "MOp5",
    "Primary motor area, layer 6a": "MOp6a",
    "Secondary motor area, layer 5": "MOs5",
    "Secondary motor area, layer 6a": "MOs6a",
    "Primary somatosensory area, mouth, layer 6a": "SSp-m6a",
    "Supplemental somatosensory area, layer 5": "SSs5",
    # Auditory cortex
    "Primary auditory area, layer 6a": "AUDp6a",
    # Prefrontal, cingulate, insular, orbital cortex
    "Prelimbic area, layer 5": "PL5",
    "Infralimbic area, layer 5": "ILA5",
    "Anterior cingulate area, dorsal part, layer 5": "ACAd5",
    "Anterior cingulate area, ventral part, layer 5": "ACAv5",
    "Agranular insular area, dorsal part, layer 5": "AId5",
    "Agranular insular area, posterior part, layer 2/3": "AIp2/3",
    "Orbital area, ventrolateral part, layer 2/3": "ORBvl2/3",
    "Orbital area, ventrolateral part, layer 6a": "ORBvl6a",
    # White matter and non-tissue labels, kept so they are recognised rather
    # than reported as unmapped. These are never valid injection zones.
    "corpus callosum, body": "ccb",
    "corpus callosum, splenium": "ccs",
    "alveus": "alv",
    "fiber tracts": "fiber tracts",
    "optic radiation": "or",
    "void": "void",
    "root": "root",
}

# Labels that name tissue no unit should be injected into, or no tissue at all.
NON_INJECTABLE_ACRONYMS = frozenset({
    # Hand-authored entries.
    "ccb", "ccs", "alv", "fiber tracts", "or", "void", "root",
    # White-matter entries added by the derived layer. Keeping these here is
    # load-bearing: an expanded vocabulary must not make a newly recognised
    # fibre tract look like an admissible injection zone.
    "ec", "ee", "fp", "int", "opt", "rust", "SCdw", "SCiw", "scp", "scwm",
})


def normalise(label):
    """Reduce a structure label to a punctuation- and case-insensitive key.

    Args:
        label: an Allen CCF long name, from either vocabulary spelling.

    Returns:
        A lowercase key with commas and periods removed and whitespace
        collapsed, suitable for dictionary lookup.
    """
    return _SPACE_RE.sub(" ", _PUNCT_RE.sub("", str(label))).strip().lower()


_NORMALISED = {normalise(name): acronym for name, acronym in NAME_TO_ACRONYM.items()}


def to_acronym(label, default=None, include_derived=False):
    """Translate a host-side CCF long name into a donor-side acronym.

    Args:
        label: the ``location`` string from an NWB electrodes table.
        default: value returned when the label is not in the table.
        include_derived: also consult the derived layer built by
            ``derive_ccf_label_map.py``. Off by default so that callers written
            against the hand-authored table keep exactly their original
            behaviour; the hand-authored entry always wins where both define a
            label. Use ``provenance`` to report which layer answered.

    Returns:
        The template-library acronym, or ``default`` when unmapped. Callers
        should report unmapped labels rather than silently discarding them.
    """
    key = normalise(label)
    if key in _NORMALISED:
        return _NORMALISED[key]
    if include_derived and key in _DERIVED_NORMALISED:
        return _DERIVED_NORMALISED[key]
    return default


# ---------------------------------------------------------------------------
# The derived layer.
#
# The hand-authored table above covers the structures a CA1-targeted search
# needs. It does not cover the host vocabulary the region-unaware arm meets,
# and the obvious fix -- importing the Allen CCF ontology -- is not available
# to this project: the Allen Institute Terms of Use permit noncommercial use
# only and forbid commercial redistribution without written permission, which
# Dandelion's licensing standard does not accept by default.
#
# ``derive_ccf_label_map.py`` therefore reads the correspondence off two
# commercial-use-permitting sources the project already holds -- DANDI 000409
# (CC-BY-4.0) electrode annotations and hybrid_template_library (MIT) donor
# rows -- and writes it to the JSON beside this module.
#
# The derived layer is **opt-in on every call**. ``to_acronym`` keeps its
# original hand-authored-only behaviour by default, so a caller written before
# this layer existed cannot silently change meaning underneath itself. Ask for
# the derived entries explicitly, and use ``provenance`` to report which layer
# answered.
# ---------------------------------------------------------------------------

DERIVED_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "ccf_label_map_derived.json")

HAND_AUTHORED = "hand-authored"


def _load_derived(path=DERIVED_PATH):
    """Load the derived map written by ``derive_ccf_label_map.py``.

    Args:
        path: JSON file to read. Defaults to the copy beside this module.

    Returns:
        A tuple of (metadata dict, entries dict). Both are empty when the file
        is absent, which keeps this module importable in a checkout that has
        not run the derivation yet.
    """
    if not os.path.exists(path):
        return {}, {}
    with open(path, encoding="utf-8") as handle:
        document = json.load(handle)
    entries = document.pop("entries", {})
    return document, entries


DERIVED_META, DERIVED_ENTRIES = _load_derived()

_DERIVED_NORMALISED = {normalise(name): entry["acronym"]
                       for name, entry in DERIVED_ENTRIES.items()}
_DERIVED_TIER = {normalise(name): entry["tier"] for name, entry in DERIVED_ENTRIES.items()}


def provenance(label):
    """Say which layer defines a host label, without resolving it.

    Args:
        label: the ``location`` string from an NWB electrodes table.

    Returns:
        ``"hand-authored"``, ``"derived:unanimous"``, ``"derived:majority"``,
        or None when no layer defines it. Callers reporting a region
        assignment should state this rather than presenting both layers as
        equally established: the hand-authored entries were validated against
        independent evidence, and the derived ones were read off that evidence.
    """
    key = normalise(label)
    if key in _NORMALISED:
        return HAND_AUTHORED
    if key in _DERIVED_NORMALISED:
        return f"derived:{_DERIVED_TIER[key]}"
    return None


def is_injectable(acronym):
    """Return True if an acronym names tissue a unit could be injected into.

    Args:
        acronym: a template-library ``brain_area`` acronym.

    Returns:
        False for white matter, ventricle, and out-of-brain labels.
    """
    return bool(acronym) and acronym not in NON_INJECTABLE_ACRONYMS
