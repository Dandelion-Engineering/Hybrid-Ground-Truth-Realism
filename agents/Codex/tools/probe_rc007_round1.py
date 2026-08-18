"""Independently probe RC-007's decision contract and reviewer counterexamples.

The owner checker authenticates selected arithmetic and prose tokens.  This
reviewer probe addresses properties that token checks do not settle: whether
the written rules yield one disposition, whether every declared bound reaches
the pass rule, whether the peak/peak-to-peak inequality has the stated
direction, whether the sparse sampling grid can support its universal timing
claim, and whether the ideal FFT filter's edge response is actually confined
to the discarded samples.

The probe reads only tracked text and source files.  It reads no archive asset,
sample value, candidate noise value, or network resource.

Example:
    ./venv/Scripts/python.exe "agents/Codex/tools/probe_rc007_round1.py" \
        --repo-root .
"""

import argparse
import ast
import hashlib
import math
import os
import subprocess
import sys


DOC_REL = os.path.join(
    "agents", "Claude", "Tier A Host and Injection Zone Selection.md"
)
CLAIM_REL = "Claim Sheet.md"
LAYOUT_PROBE_REL = os.path.join(
    "agents", "Claude", "tools", "probe_raw_ap_layout.py"
)
OWNER_PROBE_REL = os.path.join(
    "agents", "Claude", "tools", "probe_rc007_spec.py"
)
EXPECTED_DOC_SHA256 = (
    "d0fdd4626bc3680313ddbae122a10e157d7b8efbbd9f6847752a1379fabc5bd8"
)


class Checks:
    """Collect named reviewer checks and print one bounded summary."""

    def __init__(self):
        """Create an empty check ledger."""
        self.rows = []

    def check(self, name, condition, detail=""):
        """Record one boolean check.

        Args:
            name: short ASCII check label.
            condition: truthy when the reviewer construction reproduced.
            detail: optional failure context.
        """
        self.rows.append((name, bool(condition), detail))

    def report(self):
        """Print all checks and return the failure count."""
        failed = 0
        for name, ok, detail in self.rows:
            status = "ok  " if ok else "FAIL"
            line = f"[{status}] {name}"
            if not ok and detail:
                line += " -- " + detail
            print(line)
            failed += int(not ok)
        print(f"\n{len(self.rows)} checks, {failed} failed")
        return failed


def read_bytes(path):
    """Read one file as bytes.

    Args:
        path: file path.

    Returns:
        File bytes.
    """
    with open(path, "rb") as handle:
        return handle.read()


def read_text(path):
    """Read one UTF-8 file.

    Args:
        path: file path.

    Returns:
        Decoded text.
    """
    return read_bytes(path).decode("utf-8")


def section(text, start, end=None):
    """Return text from one unique marker to another.

    Args:
        text: containing text.
        start: opening marker.
        end: optional closing marker.

    Returns:
        Selected substring.
    """
    begin = text.index(start)
    if end is None:
        return text[begin:]
    return text[begin:text.index(end, begin)]


def highpass_impulse_at(n_samples, cutoff_bin, index):
    """Return the ideal real-FFT high-pass impulse response at one index.

    Args:
        n_samples: transform length.
        cutoff_bin: highest positive-frequency bin removed, inclusive.
        index: output sample to evaluate.

    Returns:
        The real impulse-response value.  For a unit impulse, removing DC and
        positive/negative bins 1..cutoff_bin subtracts their Dirichlet kernel.
    """
    lowpass = 1.0
    for freq_bin in range(1, cutoff_bin + 1):
        lowpass += 2.0 * math.cos(
            2.0 * math.pi * freq_bin * index / n_samples
        )
    delta = 1.0 if index == 0 else 0.0
    return delta - lowpass / n_samples


def main(argv=None):
    """Run the independent RC-007 Round-1 checks.

    Args:
        argv: optional command-line argument list.

    Returns:
        Zero when every reviewer construction reproduced.
    """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--repo-root", required=True, help="repository root")
    args = parser.parse_args(argv)
    root = os.path.abspath(args.repo_root)
    doc_path = os.path.join(root, DOC_REL)
    claim_path = os.path.join(root, CLAIM_REL)
    layout_probe_path = os.path.join(root, LAYOUT_PROBE_REL)
    owner_probe_path = os.path.join(root, OWNER_PROBE_REL)

    doc_bytes = read_bytes(doc_path)
    doc = doc_bytes.decode("utf-8")
    claim = read_text(claim_path)
    sec19 = section(doc, "## 19. ")
    pass_rule = section(
        sec19,
        "**The pass rule uses the level, the spread, and the estimator's resolution.**",
        "### 19.7",
    )
    checks = Checks()

    checks.check(
        "candidate document digest authenticated",
        hashlib.sha256(doc_bytes).hexdigest() == EXPECTED_DOC_SHA256,
    )

    owner = subprocess.run(
        [sys.executable, owner_probe_path, "--repo-root", root],
        capture_output=True,
        text=True,
        check=False,
    )
    checks.check(
        "owner checker is green on the authenticated candidate",
        owner.returncode == 0 and "99 checks, 0 failed" in owner.stdout,
    )

    checks.check(
        "green owner checker misses stale 12.5-to-25 ladder",
        "`12.5 → 25.0 µV`" in sec19 and owner.returncode == 0,
    )

    checks.check(
        "declared 1.25 lower bound is absent from the pass rule",
        "1.25 µV ≤ sigma_worst" in sec19
        and "sigma_worst ≥" not in pass_rule
        and "1.25" not in pass_rule,
    )

    # A single-sided peak of 30 and trough of -20 have p2p amplitude 50.
    # At sigma=1, the stated peak ceiling of 40 is satisfied, while the p2p
    # proxy rejects.  The p2p condition is therefore sufficient, not necessary.
    sigma = 1.0
    peak_snr = 30.0 / sigma
    p2p_snr = (30.0 - (-20.0)) / sigma
    checks.check(
        "peak-to-peak saturation proxy is not a necessary condition",
        peak_snr <= 40.0 and p2p_snr > 40.0,
        f"peak={peak_snr}, p2p={p2p_snr}",
    )

    # The written branches both fire on this legal numeric state and no
    # precedence is declared, so one candidate has two terminal dispositions.
    r_space = 3.0
    r_null = 3.0
    tolerance = 2.0
    fails_homogeneity = r_space > tolerance
    is_unmeasurable = r_null > tolerance
    checks.check(
        "homogeneity failure and unmeasurable branches overlap",
        fails_homogeneity
        and is_unmeasurable
        and "if `R_space > M` it fails" in pass_rule
        and "if `R_null > M` it is **unmeasurable**" in pass_rule,
    )

    # RC-007 samples only 60 of 9,999 full chunks.  A one-chunk excursion at
    # any unselected index is invisible although an injection segment can
    # contain it, contradicting the "wherever the segment lands" rationale.
    full_chunks = 9999
    k_windows = 60
    sampled = {math.floor(k * full_chunks / k_windows) for k in range(k_windows)}
    missed_chunk = next(index for index in range(full_chunks) if index not in sampled)
    baseline = [1.0] * full_chunks
    baseline[missed_chunk] = 100.0
    sampled_max = max(baseline[index] for index in sampled)
    checks.check("sampling grid has 60 unique windows", len(sampled) == 60)
    checks.check(
        "unsampled full-chunk excursion defeats the wherever claim",
        sampled_max == 1.0
        and max(baseline) == 100.0
        and "requiring admissibility *wherever* the segment lands" in sec19,
        f"missed chunk {missed_chunk}",
    )

    # An ideal rectangular FFT high-pass has a global Dirichlet-kernel impulse
    # response.  A unit impulse at the edge remains non-zero at the retained
    # centre, far beyond the 150-sample discard.
    n_samples = 13020
    cutoff_bin = 130  # bins strictly below 300 Hz at 30 kHz and N=13,020
    centre = n_samples // 2
    centre_response = highpass_impulse_at(n_samples, cutoff_bin, centre)
    checks.check(
        "brick-wall FFT edge response reaches the retained centre",
        centre > 150
        and centre < n_samples - 150
        and abs(centre_response) > 1e-8
        and "the wrap is confined to the edges" in sec19,
        f"h[{centre}]={centre_response:.12g}",
    )

    # The in-force Claim Sheet explicitly makes effective SNR a per-donor hard
    # host-specific eligibility gate that determines N.  Relabelling it a
    # donor quantity therefore does not establish that it has no independent
    # rejection power over the host-dependent Tier-A configuration.
    checks.check(
        "Claim Sheet retains effective SNR as hard host-specific eligibility",
        "per-donor hard host-specific eligibility gates" in claim
        and "effective host SNR" in claim
        and "`N < 10` fails Tier A" in claim,
    )
    checks.check(
        "Draft 29 removes that gate from host admissibility",
        "four gates rather than five" in sec19
        and "The substantive part of gate 3 is real" in sec19,
    )

    source = read_text(layout_probe_path)
    tree = ast.parse(source, filename=layout_probe_path)
    sample_reads = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Subscript)
        and isinstance(node.value, ast.Name)
        and node.value.id == "data"
    ]
    checks.check(
        "layout probe has no Python-level data-dataset slice",
        len(sample_reads) == 0,
        f"found {len(sample_reads)} data subscripts",
    )

    failed = checks.report()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
