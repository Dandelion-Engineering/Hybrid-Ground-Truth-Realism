"""Check the structural policy consequences of the Part-B split family.

Claude Session 52 showed that the 32 block-interleave members can reach
different branch-4 dispositions even when every per-channel ratio is finite.
This probe asks a narrower design question: whether any member has an
outcome-independent interpretation that the other members do not, and what
the two extremal multi-member rules reduce to on the authenticated ramp-band
record.

The result is not a Part-B candidate and does not approve a split. It checks
three facts used in Codex Session 52's design reply:

1. The midpoint member p=6510 is uniquely the partition into two contiguous,
   equal-duration epochs. Every other family member fragments both halves.
2. Choosing that member by the number of temporal runs reads only the declared
   sample geometry, never a candidate value.
3. On Claude's fully defined ramp band, choosing the largest observed upper
   value is exactly the unanimity disposition and choosing the smallest is
   exactly the existential disposition. Those data-dependent extrema disagree
   on the same bytes, while the geometry-only selector is fixed in advance.

Boundary: the ramp band is constructed. The probe establishes a structural
interpretation and selector identities, not real-recording frequency, power,
or safety. No archive, network resource, or candidate sample is read.

Usage:

    ./venv/Scripts/python.exe \
        agents/Codex/tools/probe_part_b_policy.py \
        --member-script <path> \
        --member-record <path> \
        --out <path> [--records <path>]
"""

import argparse
import hashlib
import json
import math


HALF = 6510
RETAINED = 2 * HALF
M_STRICT = 2.0
PINNED_SCRIPT_SHA256 = (
    "b653bc0c214f6a0c419489bafde244185d4bd61acc882b64e9edd2baa75a6f42"
)
PINNED_RECORD_SHA256 = (
    "4a86a090386bedd89f2d176abfdf0652ba3fe7f1bb3e29dd800d73b09e14b4fd"
)


class Checks:
    """Collect deterministic checks and render the project console format."""

    def __init__(self):
        """Initialize an empty check ledger."""
        self.lines = []
        self.failed = 0

    def heading(self, value):
        """Append a section heading.

        Inputs: `value`, heading text.
        Returns: None.
        """
        self.lines.extend(["", value])

    def note(self, value):
        """Append a non-check evidence note.

        Inputs: `value`, note text.
        Returns: None.
        """
        self.lines.append("NOTE  " + value)

    def check(self, name, condition, detail=""):
        """Record one pass or failure.

        Inputs: `name`, the checked claim; `condition`, its truth value;
        `detail`, optional measured context.
        Returns: the boolean condition.
        """
        if not condition:
            self.failed += 1
        suffix = "  [%s]" % detail if detail else ""
        self.lines.append("%s  %s%s" %
                          ("PASS" if condition else "FAIL", name, suffix))
        return condition

    def render(self):
        """Render the full ledger and count summary.

        Inputs: none.
        Returns: the report string with one trailing newline.
        """
        total = sum(line.startswith(("PASS", "FAIL")) for line in self.lines)
        return "%s\n\nSummary\n%d checks, %d failed\n" % (
            "\n".join(self.lines), total, self.failed)


def parse_args(argv=None):
    """Parse command-line paths.

    Inputs: `argv`, an optional argument sequence.
    Returns: the parsed argparse namespace.
    """
    parser = argparse.ArgumentParser(
        description=("Check outcome-independent and data-dependent policy "
                     "consequences of the Part-B split family."))
    parser.add_argument("--member-script", required=True,
                        help="Claude Session-52 member-comparison source")
    parser.add_argument("--member-record", required=True,
                        help="Claude Session-52 member-comparison JSON record")
    parser.add_argument("--out", required=True,
                        help="path for the plain-text report")
    parser.add_argument("--records", default=None,
                        help="optional path for the JSON record")
    return parser.parse_args(argv)


def sha256_of(path):
    """Compute a file's SHA-256 digest.

    Inputs: `path`, a filesystem path.
    Returns: the lowercase hexadecimal digest.
    """
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def divisors(value):
    """Return every positive divisor of an integer in increasing order.

    Inputs: `value`, a positive integer.
    Returns: the sorted divisor list.
    """
    found = set()
    for candidate in range(1, int(math.sqrt(value)) + 1):
        if value % candidate == 0:
            found.add(candidate)
            found.add(value // candidate)
    return sorted(found)


def labels_for(member):
    """Construct the declared block-interleave half labels.

    Inputs: `member`, the block length p, which must divide HALF.
    Returns: a tuple of zero/one labels of length RETAINED.
    """
    if HALF % member:
        raise ValueError("member must divide %d" % HALF)
    return tuple((index // member) % 2 for index in range(RETAINED))


def run_count(labels):
    """Count contiguous runs in a non-empty label sequence.

    Inputs: `labels`, a non-empty sequence.
    Returns: the positive integer run count.
    """
    if not labels:
        raise ValueError("labels must not be empty")
    return 1 + sum(left != right
                   for left, right in zip(labels[:-1], labels[1:]))


def positions_are_one_interval(labels, target):
    """Test whether one label occupies exactly one contiguous interval.

    Inputs: `labels`, a zero/one sequence; `target`, the label to inspect.
    Returns: True exactly when every target position lies between its first and
    last occurrence with no interruption.
    """
    positions = [index for index, value in enumerate(labels)
                 if value == target]
    return bool(positions) and positions == list(
        range(positions[0], positions[-1] + 1))


def load_authenticated_json(script_path, record_path):
    """Authenticate Claude's exact source and record, then load the record.

    Inputs: `script_path` and `record_path`, filesystem paths.
    Returns: `(record, measured_script_digest, measured_record_digest)`.
    Raises: SystemExit before parsing when either digest differs.
    """
    script_digest = sha256_of(script_path)
    record_digest = sha256_of(record_path)
    if script_digest != PINNED_SCRIPT_SHA256:
        raise SystemExit(
            "member script digest mismatch: expected %s, measured %s" %
            (PINNED_SCRIPT_SHA256, script_digest))
    if record_digest != PINNED_RECORD_SHA256:
        raise SystemExit(
            "member record digest mismatch: expected %s, measured %s" %
            (PINNED_RECORD_SHA256, record_digest))
    with open(record_path, "r", encoding="utf-8") as handle:
        return json.load(handle), script_digest, record_digest


def main(argv=None):
    """Run the policy checks and write deterministic records.

    Inputs: `argv`, an optional argument sequence.
    Returns: zero when every check passes, otherwise one.
    """
    args = parse_args(argv)
    source, script_digest, record_digest = load_authenticated_json(
        args.member_script, args.member_record)
    checks = Checks()
    records = {
        "authenticated_script_sha256": script_digest,
        "authenticated_record_sha256": record_digest,
        "half_samples": HALF,
        "retained_samples": RETAINED,
        "threshold_m": M_STRICT,
    }

    checks.heading("1. Family geometry and the unique contiguous member")
    members = divisors(HALF)
    recorded_members = [int(value) for value in source["members"]]
    checks.check("the independently derived family equals the authenticated "
                 "32-member record",
                 members == recorded_members and len(members) == 32,
                 "%d members" % len(members))

    geometry = []
    for member in members:
        labels = labels_for(member)
        count_zero = labels.count(0)
        count_one = labels.count(1)
        total_runs = run_count(labels)
        both_contiguous = (positions_are_one_interval(labels, 0)
                           and positions_are_one_interval(labels, 1))
        geometry.append({
            "member": member,
            "zero_samples": count_zero,
            "one_samples": count_one,
            "total_runs": total_runs,
            "both_halves_contiguous": both_contiguous,
        })

    checks.check("every member partitions the retained core into two disjoint "
                 "equal-size halves",
                 all(row["zero_samples"] == HALF
                     and row["one_samples"] == HALF for row in geometry),
                 "%d samples in each half" % HALF)
    contiguous = [row["member"] for row in geometry
                  if row["both_halves_contiguous"]]
    checks.check("p = 6510 is uniquely the partition into two contiguous "
                 "equal-duration epochs",
                 contiguous == [HALF],
                 "contiguous members %s" % contiguous)
    minimum_runs = min(row["total_runs"] for row in geometry)
    minimum_run_members = [row["member"] for row in geometry
                           if row["total_runs"] == minimum_runs]
    checks.check("the geometry-only minimum-fragmentation selector therefore "
                 "chooses p = 6510 without reading any signal value",
                 minimum_runs == 2 and minimum_run_members == [HALF],
                 "minimum %d runs at %s" %
                 (minimum_runs, minimum_run_members))
    checks.check("every other member fragments the epochs into at least four "
                 "alternating runs",
                 all(row["total_runs"] >= 4 for row in geometry
                     if row["member"] != HALF),
                 "next-smallest run count %d" %
                 min(row["total_runs"] for row in geometry
                     if row["member"] != HALF))
    records["geometry"] = geometry

    checks.heading("2. Extremal data-dependent selectors on the ramp band")
    ramp = source["ramp_band"]
    values = {int(member): float(value)
              for member, value in ramp["reported_values"].items()}
    stand_down = sorted(int(value) for value in ramp["stand_down_members"])
    withhold = sorted(int(value) for value in ramp["withholding_members"])
    undefined = sorted(int(value) for value in ramp["undefined_members"])
    derived_stand_down = sorted(member for member, value in values.items()
                                if value <= M_STRICT)
    derived_withhold = sorted(member for member, value in values.items()
                              if value > M_STRICT)
    checks.check("all 32 ramp-band values are finite and defined",
                 set(values) == set(members) and not undefined
                 and all(math.isfinite(value) for value in values.values()),
                 "%d values, %d undefined" %
                 (len(values), len(undefined)))
    checks.check("the authenticated dispositions are exactly the thresholded "
                 "reported values",
                 stand_down == derived_stand_down
                 and withhold == derived_withhold,
                 "%d stand down, %d withhold" %
                 (len(stand_down), len(withhold)))

    minimum_value = min(values.values())
    maximum_value = max(values.values())
    minimum_members = sorted(member for member, value in values.items()
                             if value == minimum_value)
    maximum_members = sorted(member for member, value in values.items()
                             if value == maximum_value)
    existential_stands_down = minimum_value <= M_STRICT
    unanimity_stands_down = maximum_value <= M_STRICT
    checks.check("choosing the smallest observed member value is exactly the "
                 "existential rule on this band",
                 existential_stands_down
                 == any(value <= M_STRICT for value in values.values()),
                 "minimum %.6f at %s" %
                 (minimum_value, minimum_members))
    checks.check("choosing the largest observed member value is exactly the "
                 "unanimity rule on this band",
                 unanimity_stands_down
                 == all(value <= M_STRICT for value in values.values()),
                 "maximum %.6f at %s" %
                 (maximum_value, maximum_members))
    checks.check("the two outcome-reading extrema reach opposite dispositions "
                 "on byte-identical fully defined data",
                 existential_stands_down and not unanimity_stands_down,
                 "existential stands down; unanimity withholds")
    checks.check("the geometry-only selector is p = 6510 regardless of those "
                 "values and its ramp disposition is withholding",
                 minimum_run_members == [HALF]
                 and values[HALF] > M_STRICT,
                 "p=6510 value %.6f" % values[HALF])

    records["ramp_policy"] = {
        "minimum_value": minimum_value,
        "minimum_members": minimum_members,
        "maximum_value": maximum_value,
        "maximum_members": maximum_members,
        "existential_stands_down": existential_stands_down,
        "unanimity_stands_down": unanimity_stands_down,
        "geometry_selected_member": HALF,
        "geometry_selected_value": values[HALF],
        "geometry_selected_stands_down": values[HALF] <= M_STRICT,
        "stand_down_members": stand_down,
        "withholding_members": withhold,
    }

    checks.heading("3. Decision boundary")
    checks.note("the unique contiguous member has an outcome-independent "
                "temporal meaning: early epoch versus late epoch")
    checks.note("unanimity is a predeclared worst-member functional, not a "
                "partition-invariant estimate; on the ramp band its verdict "
                "is set by p = 6510")
    checks.note("a selector that reads member values needs its own scientific "
                "criterion and selection-aware evidence; a selector that "
                "reads geometry alone reduces to a fixed pin")
    checks.note("all ramp-band values are constructed; no real-data frequency, "
                "power, or safety claim follows")
    records["boundary"] = (
        "constructed authenticated ramp band plus sample geometry only; no "
        "archive, candidate, frequency, power, or safety claim"
    )

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
