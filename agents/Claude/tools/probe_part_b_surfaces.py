"""Mechanically count every live Part-B surface in frozen Draft 34.

Codex's Session-51 scope ruling put both section 19.6's decision vocabulary and
the Part-B-owned publication clauses of section 19.7 inside the eventual
successor card, and required that the directly affected current-live statements
be counted MECHANICALLY before any candidate is called stable. His Session-52
design ruling made the same requirement its first ordered step: count and
rewrite every live Part-B surface under the narrowed name and claim, and only
then let the state sit before formal review.

THIS PROBE IS THE COUNT. It rewrites nothing, proposes no candidate, edits no
section and opens no Review Card. It authenticates the frozen document by
digest and refuses to run if a single byte has moved, because an inventory
taken against a different state is worse than no inventory.

How the extraction is made mechanical rather than asserted:

  1. TWO TOKEN TIERS, AND THE SECOND IS JUSTIFIED BY A CHECK ON THE FIRST. The
     tier-1 tokens are the identifiers that name the Part-B objects and nothing
     else - `R_null_sampled`, `r_c`, the two half-window scales and the
     per-window series. They are searched over the WHOLE document, and the
     probe checks that every occurrence falls inside section 19 or the status
     stack. Only because that check passes is it legitimate to search the
     broader vocabulary - split, contiguous, interleaving, branch 4, the two
     branch-3 labels, unmeasurable, half, 6,510 - inside section 19 alone. The
     restriction is derived, not assumed, which is the difference between a
     count and a guess.

  2. THE UNIT IS THE SENTENCE, AND THE SPLITTER IS PINNED. Live section bodies
     are split into sentences by one fixed rule; table rows are single units.
     Every unit that carries any token is extracted and keyed by the digest of
     its own text, so the inventory cannot drift while the document is frozen
     and cannot silently survive a change to it.

  3. THE CLASSIFICATION IS TOTAL IN BOTH DIRECTIONS. Each extracted unit is
     dispositioned by a pinned table into `part-b`, `mixed`, `part-a` or
     `not-a-surface`, and every `part-b` and `mixed` unit carries a rewrite
     action. The probe fails if any extracted unit lacks an entry OR if any
     entry matches no extracted unit. Classification is judgement; its
     completeness is not.

What the count establishes:

  - Codex's named scope is exactly right. Every Part-B and mixed unit lies in
    section 19.5, 19.6, 19.7 or 19.10 and nowhere else, and no tier-1 token
    appears anywhere outside section 19 and the status stack.
  - The rewrite is larger than a rename. Fifteen units state a GROUND for the
    contiguous split, and the ground the frozen text calls "the whole of the
    reason" is the free-parameter argument RC-008's F8-R3 withdrew - so the
    document currently pins the rule on a ground it has itself retracted.
  - One unit is the sentence Session 50 proved FALSE: section 19.6's "No
    undefined ratio enters a comparison". It is carried here as its own
    action so it cannot be lost inside a rename pass.
  - The historical surfaces are counted and excluded by a mechanical rule
    rather than by memory: the status-line stack and sections 19.11 to 19.15
    are the append-only record and are not rewrite targets.

NO FORMAL REVIEW HAS SEEN THIS PROBE. It was written outside the review cycle
as preparation for a Part B that has no candidate and no Review Card. The
inventory is evidence for that work and is not an approved state of anything.

BOUNDARY. This probe reads one project document and nothing else. It makes no
claim about what any sentence should say, only about which sentences are in
scope and what kind of change each needs. The classification is one agent's
reading, offered for review; only its totality is mechanical.

Usage:

    ./venv/Scripts/python.exe \\
        agents/Claude/tools/probe_part_b_surfaces.py \\
        --document <path> --out <path> [--records <path>]
"""

import argparse
import hashlib
import json
import re

# The exact frozen state this inventory is taken against. Draft 34 has not been
# edited since Session 48 and must not be edited to make this probe pass.
PINNED_DOCUMENT_SHA256 = (
    "ecccfa565966276e203efef2794f180fe73a2e1e0cbc8beff97d3bd8916a6f89")

# Identifiers that name a Part-B object and nothing else. The Greek and
# combining characters are written as escapes so this source stays pure ASCII
# on disk and does not depend on the reader's locale to be opened correctly.
TIER1_TOKENS = ["R_null_sampled", "r_c", "\u03c1(k)",
                "\u03c3\u0302_c^A", "\u03c3\u0302_c^B"]

# The surrounding vocabulary, searched inside section 19 only, which is
# legitimate exactly because the tier-1 check below passes.
TIER2_TOKENS = ["split", "interleav", "contiguous", "6,510", "branch 4",
                "resolution-limited", "resolved heterogeneity",
                "unmeasurable", "half"]

# Sections whose text is live specification. Sections 19.11 to 19.15 are the
# append-only draft-change record and the status stack sits above section 0;
# neither is a rewrite target.
LIVE_SECTIONS = ["19.1", "19.2", "19.3", "19.4", "19.5", "19.6", "19.7",
                 "19.8", "19.9", "19.10"]
HISTORICAL_SECTIONS = ["19.11", "19.12", "19.13", "19.14", "19.15"]

CLASSES = ("part-b", "mixed", "part-a", "not-a-surface")
ACTIONS = ("rename", "ground", "claim", "semantics", "publication",
           "false-sentence")

# The pinned classification, keyed on the first sixteen hexadecimal digits of
# each unit's own SHA-256. Every entry is (class, primary action, secondary
# action or None). Distinctness of the sixteen-digit keys is checked below.
CLASSIFICATION = {
    # --- section 19.2: incidental vocabulary, not a Part-B surface ----------
    "857026c3c9b64495": ("not-a-surface", None, None),
    "ee19655477513e70": ("not-a-surface", None, None),
    # --- section 19.5: the definition, the estimand, the grounds -----------
    "b3bb22e5daece73c": ("part-b", "claim", "rename"),
    "eb5e18231d5f2d41": ("part-b", "rename", "semantics"),
    "f99e8f437bc4484f": ("part-b", "claim", None),
    "b4a02f6400c08a13": ("part-b", "claim", None),
    "6e4da48dce3f5b27": ("part-b", "rename", None),
    "a9b771c35f499275": ("mixed", "rename", None),
    "52b2078b202d639d": ("part-b", "rename", None),
    "505b633576508b9a": ("part-b", "rename", "claim"),
    "983a7eb413d9dfcb": ("part-b", "rename", None),
    "e0039ff0f036f2bf": ("part-b", "ground", None),
    "9e964a38c978973b": ("part-b", "ground", None),
    "afe7648e0218cc32": ("part-b", "ground", None),
    "ff29184e1fb85721": ("part-b", "ground", None),
    "bfc234da71147847": ("part-b", "ground", "claim"),
    "4de76ae345d4d682": ("part-b", "ground", None),
    "e0e86d1a236a89df": ("part-b", "ground", None),
    "b1969829e8071867": ("part-b", "ground", None),
    "583dacbccdb2932e": ("part-b", "ground", None),
    "ec568b977332ba6a": ("part-b", "claim", None),
    "09e3e4268e47a83b": ("part-b", "rename", None),
    "2fdb82eff245282b": ("part-b", "claim", None),
    "6f84caebe9d38b37": ("part-b", "ground", None),
    "45fdf94bb7b35d1f": ("part-b", "ground", None),
    "b9096e9ed729a21c": ("mixed", "ground", "publication"),
    "400b36b62cfbd6dc": ("part-b", "claim", None),
    "18961c272df0d47b": ("part-b", "claim", None),
    "3da07521b144f80e": ("part-b", "rename", None),
    "d1ec6e5f67386ace": ("part-b", "rename", None),
    "36dd9fd7c6a7d761": ("part-b", "claim", None),
    "f401d931747f2ba0": ("part-b", "rename", None),
    "a9f2abca9dccf225": ("part-b", "rename", None),
    # --- section 19.6: the pre-declared parameter and the branches ---------
    "aa56e4602ad57039": ("part-b", "claim", "rename"),
    "da12b137066b08a4": ("not-a-surface", None, None),
    "4e69762901214597": ("mixed", "rename", None),
    "18b4645eb576d892": ("mixed", "rename", None),
    "99dc110363657307": ("part-b", "rename", "semantics"),
    "be06fcd76f0653f2": ("part-b", "rename", None),
    "28adcd864b1d5e80": ("part-b", "rename", "semantics"),
    "3f1c1404da183d76": ("part-b", "rename", None),
    "032dfedc3ca2dffa": ("part-b", "rename", None),
    "2409b6041d32604b": ("part-b", "false-sentence", "semantics"),
    "93816031eb3b0a8b": ("mixed", "semantics", None),
    # --- section 19.7: the publication surface -----------------------------
    "db777be9ba03bb2b": ("mixed", "publication", "rename"),
    "05b29556183f3924": ("mixed", "publication", None),
    # --- section 19.8: incidental vocabulary -------------------------------
    "794405d3f765c0ee": ("not-a-surface", None, None),
    "7f2d6f4ad3440a22": ("not-a-surface", None, None),
    # --- section 19.10: the boundaries -------------------------------------
    "16f7e52209b71eff": ("part-b", "rename", None),
    "53798e56a8f0ccd1": ("mixed", "rename", None),
    "51405c8e852c6a28": ("part-b", "ground", "claim"),
    "70ab7ad91ea4456a": ("part-b", "ground", None),
    "d17d5b9221eb2916": ("part-b", "claim", None),
    "769e1ac41fe79761": ("part-b", "ground", None),
    "28d6e14c943919dc": ("part-b", "claim", None),
    "bab48c7b1654313b": ("part-b", "claim", None),
    "fb3fbc94b926883a": ("part-b", "rename", None),
    "bb036bf4948bf554": ("not-a-surface", None, None),
}

# The three units the rewrite must not lose inside a rename pass, named by
# digest so that a change to any of them fails this probe rather than passing
# quietly. The first is the sentence Session 50 proved false; the other two are
# the ground RC-008's F8-R3 withdrew, which the frozen text still calls the
# whole of the reason.
NAMED_UNITS = {
    "2409b6041d32604b": "section 19.6's no-undefined-ratio sentence",
    "6f84caebe9d38b37": "section 19.5's free-parameter ground",
    "45fdf94bb7b35d1f": "section 19.5's whole-of-the-reason sentence",
}


class Checks(object):
    """Collect pass/fail lines and print them in the project's console form."""

    def __init__(self):
        self.lines = []
        self.failed = 0

    def heading(self, text):
        """Append a blank line and a section heading."""
        self.lines.append("")
        self.lines.append(text)

    def note(self, text):
        """Append a line that is deliberately NOT a check."""
        self.lines.append("NOTE  " + text)

    def check(self, name, ok, detail=""):
        """Record one check; `detail` is printed either way."""
        if not ok:
            self.failed += 1
        self.lines.append("%s  %s%s" % ("PASS" if ok else "FAIL", name,
                                        ("  [%s]" % detail) if detail else ""))
        return ok

    def render(self):
        """Return the full report with the trailing check-count summary."""
        body = "\n".join(self.lines)
        total = sum(1 for line in self.lines
                    if line.startswith("PASS") or line.startswith("FAIL"))
        return "%s\n\nSummary\n%d checks, %d failed\n" % (body, total,
                                                          self.failed)


def sha256_of_bytes(payload):
    """SHA-256 of a byte string.

    Inputs: `payload`, the bytes.
    Returns: the lowercase hex digest.
    """
    return hashlib.sha256(payload).hexdigest()


def authenticate_document(path):
    """Read the frozen document and check its pinned digest.

    Inputs: `path`, the document path.
    Returns: the decoded text.
    Raises: SystemExit when the digest differs, because an inventory taken
    against a different state would be silently wrong rather than loudly so.
    """
    with open(path, "rb") as handle:
        payload = handle.read()
    measured = sha256_of_bytes(payload)
    if measured != PINNED_DOCUMENT_SHA256:
        raise SystemExit(
            "document digest mismatch: pinned %s, measured %s" %
            (PINNED_DOCUMENT_SHA256, measured))
    return payload.decode("utf-8"), measured


def split_sentences(paragraph):
    """Split one markdown paragraph into sentences by the pinned rule.

    Inputs: `paragraph`, one line of the document.
    Returns: the list of sentences.

    The rule is a period or colon followed by whitespace and then a capital
    letter, a backtick, an asterisk, a section mark or an opening quote. It is
    pinned rather than tuned: the inventory's job is a stable partition of the
    text, not a linguistically perfect one, and every produced unit is keyed by
    its own digest so a change to the rule is visible as a changed key.
    """
    parts = re.split(r"(?<=[.:])\s+(?=[A-Z`*\u00a7\u201c\"])", paragraph)
    return [part for part in parts if part.strip()]


def walk_sections(text):
    """Attribute every non-blank line to its section number.

    Inputs: `text`, the whole document.
    Returns: a list of `(section, line_number, line)` triples, where `section`
    is a numbered subsection string, the literal `status-stack` for lines above
    the first heading, or None for a top-level section body.
    """
    rows = []
    section = "status-stack"
    for number, line in enumerate(text.split("\n"), 1):
        subsection = re.match(r"^###\s+(\d+\.\d+)\s", line)
        if subsection:
            section = subsection.group(1)
            continue
        if re.match(r"^##\s", line):
            section = None
            continue
        if line.strip():
            rows.append((section, number, line))
    return rows


def units_in(rows, sections, tier1, tier2):
    """Extract every token-bearing unit from the named sections.

    Inputs: `rows`, the output of `walk_sections`; `sections`, the section
    numbers to read; `tier1` and `tier2`, the token lists.
    Returns: a list of dicts, one per extracted unit.
    """
    found = []
    for section, number, line in rows:
        if section not in sections:
            continue
        pieces = ([line] if line.lstrip().startswith("|")
                  else split_sentences(line))
        for piece in pieces:
            hits1 = [token for token in tier1 if token in piece]
            hits2 = [token for token in tier2 if token in piece]
            if not hits1 and not hits2:
                continue
            found.append({
                "section": section,
                "line": number,
                "key": sha256_of_bytes(piece.encode("utf-8"))[:16],
                "tier1": hits1,
                "tier2": hits2,
                "text": piece[:160],
            })
    return found


def parse_args(argv=None):
    """Parse the command line.

    Inputs: `argv`, an optional argument list.
    Returns: the parsed namespace.
    """
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--document", required=True,
                        help="path to the Tier A selection document")
    parser.add_argument("--out", required=True,
                        help="path for the plain-text report")
    parser.add_argument("--records", default=None,
                        help="optional path for the JSON record")
    return parser.parse_args(argv)


def main(argv=None):
    """Run every check, print the report and write the artifacts."""
    args = parse_args(argv)
    text, digest = authenticate_document(args.document)
    rows = walk_sections(text)
    checks = Checks()
    records = {"document_sha256": digest,
               "live_sections": LIVE_SECTIONS,
               "historical_sections": HISTORICAL_SECTIONS}

    # ------------------------------------------------------------------
    checks.heading("1. Where the Part-B identifiers are, document-wide")

    tier1_by_section = {}
    for section, _number, line in rows:
        for token in TIER1_TOKENS:
            count = line.count(token)
            if count:
                label = section if section else "(top-level body)"
                tier1_by_section.setdefault(label, {})
                tier1_by_section[label][token] = (
                    tier1_by_section[label].get(token, 0) + count)
    records["tier1_by_section"] = tier1_by_section

    permitted = set(LIVE_SECTIONS) | set(HISTORICAL_SECTIONS) | {"status-stack"}
    stray = sorted(label for label in tier1_by_section
                   if label not in permitted)
    checks.check("every Part-B identifier in the document lies in section 19 "
                 "or the status stack, so restricting the broader vocabulary "
                 "to section 19 is derived rather than assumed",
                 stray == [],
                 "%d sections carry one, no strays" % len(tier1_by_section))

    live_labels = sorted(label for label in tier1_by_section
                         if label in set(LIVE_SECTIONS))
    historical_labels = sorted(label for label in tier1_by_section
                               if label in set(HISTORICAL_SECTIONS)
                               or label == "status-stack")
    checks.check("the identifiers appear in exactly four live subsections",
                 live_labels == ["19.10", "19.5", "19.6", "19.7"],
                 "live: %s" % ", ".join(live_labels))
    checks.check("and in the append-only record, which the rewrite must not "
                 "touch",
                 set(historical_labels) == (set(HISTORICAL_SECTIONS)
                                            | {"status-stack"}),
                 "historical: %s" % ", ".join(historical_labels))

    # ------------------------------------------------------------------
    checks.heading("2. The extraction, and that the classification is total")

    live = units_in(rows, set(LIVE_SECTIONS), TIER1_TOKENS, TIER2_TOKENS)
    historical = units_in(rows, set(HISTORICAL_SECTIONS) | {"status-stack"},
                          TIER1_TOKENS, TIER2_TOKENS)
    records["live_units"] = live
    records["historical_unit_count"] = len(historical)

    keys = [unit["key"] for unit in live]
    checks.check("every extracted unit has a distinct digest key, so the "
                 "sixteen-digit prefix is a safe identifier here",
                 len(set(keys)) == len(keys),
                 "%d units, %d distinct keys" % (len(keys), len(set(keys))))
    missing = sorted(key for key in keys if key not in CLASSIFICATION)
    checks.check("every extracted live unit carries a classification entry",
                 missing == [],
                 "%d unclassified" % len(missing))
    unused = sorted(key for key in CLASSIFICATION if key not in set(keys))
    checks.check("every classification entry matches an extracted unit, so "
                 "the table cannot carry a stale row",
                 unused == [],
                 "%d unused entries" % len(unused))
    checks.check("every class and every action comes from the declared "
                 "vocabulary",
                 all(row[0] in CLASSES for row in CLASSIFICATION.values())
                 and all(action is None or action in ACTIONS
                         for row in CLASSIFICATION.values()
                         for action in row[1:]),
                 "%d classes, %d actions" % (len(CLASSES), len(ACTIONS)))
    checks.check("every part-b and mixed unit carries a primary action, and "
                 "no other unit does",
                 all((row[1] is not None)
                     == (row[0] in ("part-b", "mixed"))
                     for row in CLASSIFICATION.values()),
                 "actions attach to scope units only")

    # ------------------------------------------------------------------
    checks.heading("3. The count itself")

    by_class = {name: 0 for name in CLASSES}
    by_action = {name: 0 for name in ACTIONS}
    by_section = {}
    in_scope_sections = set()
    for unit in live:
        klass, primary, secondary = CLASSIFICATION[unit["key"]]
        unit["class"] = klass
        unit["primary_action"] = primary
        unit["secondary_action"] = secondary
        by_class[klass] += 1
        for action in (primary, secondary):
            if action:
                by_action[action] += 1
        bucket = by_section.setdefault(unit["section"],
                                       {name: 0 for name in CLASSES})
        bucket[klass] += 1
        if klass in ("part-b", "mixed"):
            in_scope_sections.add(unit["section"])
    records["by_class"] = by_class
    records["by_action"] = by_action
    records["by_section"] = by_section
    records["in_scope_sections"] = sorted(in_scope_sections)

    checks.check("the live inventory is 58 units",
                 len(live) == 58,
                 "%d units over %d subsections" %
                 (len(live), len(by_section)))
    checks.check("44 are Part-B, 8 are mixed and 6 are not surfaces at all",
                 (by_class["part-b"], by_class["mixed"],
                  by_class["not-a-surface"]) == (44, 8, 6),
                 "part-b %d, mixed %d, part-a %d, not-a-surface %d" %
                 (by_class["part-b"], by_class["mixed"], by_class["part-a"],
                  by_class["not-a-surface"]))
    checks.check("every in-scope unit lies in section 19.5, 19.6, 19.7 or "
                 "19.10, so the scope Codex named is neither short nor long",
                 sorted(in_scope_sections) == ["19.10", "19.5", "19.6",
                                               "19.7"],
                 "in scope: %s" % ", ".join(sorted(in_scope_sections)))
    checks.check("the rewrite is larger than a rename: fifteen units state a "
                 "ground for the split rule",
                 by_action["ground"] == 15,
                 "rename %d, ground %d, claim %d, semantics %d, "
                 "publication %d, false-sentence %d" %
                 (by_action["rename"], by_action["ground"],
                  by_action["claim"], by_action["semantics"],
                  by_action["publication"], by_action["false-sentence"]))
    checks.check("the append-only record carries its own units, which are "
                 "counted here and excluded from the rewrite by a section "
                 "rule rather than by memory",
                 len(historical) > 0,
                 "%d historical units, 0 rewritable" % len(historical))

    # ------------------------------------------------------------------
    checks.heading("4. The units that must not be lost inside a rename")

    present = {unit["key"]: unit for unit in live}
    for key, label in sorted(NAMED_UNITS.items()):
        unit = present.get(key)
        checks.check("the inventory still contains %s at its pinned digest"
                     % label,
                     unit is not None,
                     "" if unit is None
                     else "section %s line %d, action %s" %
                          (unit["section"], unit["line"],
                           unit["primary_action"]))
    false_unit = present.get("2409b6041d32604b")
    checks.check("the sentence Session 50 proved false is classified as its "
                 "own action rather than as an ordinary rename",
                 false_unit is not None
                 and false_unit["primary_action"] == "false-sentence",
                 "section 19.6 line %d" %
                 (false_unit["line"] if false_unit else -1))
    checks.note("the free-parameter ground was withdrawn by RC-008's F8-R3, "
                "so the frozen text currently pins the contiguous split on a "
                "ground it has itself retracted; that is what the narrowed "
                "estimand has to replace")
    checks.note("this classification is one agent's reading and is offered "
                "for review; only its totality over the extraction is "
                "mechanical")

    report = checks.render()
    print(report, end="")
    with open(args.out, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(report)
    if args.records:
        with open(args.records, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(records, handle, indent=2, sort_keys=True)
            handle.write("\n")
    return 1 if checks.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
