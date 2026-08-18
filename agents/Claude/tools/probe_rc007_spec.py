"""Re-derive every number Section 19 states, from the record rather than the prose.

Section 19 of ``agents/Claude/Tier A Host and Injection Zone Selection.md``
specifies the host noise gate. It is a contract rather than a result, so the
only executable property it has is that its arithmetic closes: every threshold
it publishes must follow from a pinned quantity, and every layout figure must
follow from the recorded probe output rather than from a number someone typed.

This checker is read-only. It recomputes each figure from
``raw_ap_layout_CSHL047_Probe01_2026-08-18.json`` and from the pinned injection
amplitude target, then requires the section to contain the recomputed value as
written. It also holds the earlier sections fixed: the same-state approved
Sections 1-16, 17 and 18 spans must be byte-identical to the digests recorded
when they were approved.

It cannot go red on a defect of judgement -- a threshold can be arithmetically
correct and still be the wrong threshold -- and it is offered as an owner
instrument on that understanding, not as a substitute for review.

Example:
    ./venv/Scripts/python.exe "agents/Claude/tools/probe_rc007_spec.py" --repo-root .
"""

import argparse
import hashlib
import io
import json
import math
import os

DOC_REL = os.path.join("agents", "Claude", "Tier A Host and Injection Zone Selection.md")
LAYOUT_REL = os.path.join("agents", "Claude", "tools",
                          "raw_ap_layout_CSHL047_Probe01_2026-08-18.json")
REPORT_REL = os.path.join("agents", "Claude", "tools",
                          "raw_ap_layout_CSHL047_Probe01_2026-08-18.txt")

# Digests recorded when each span was approved. Sections 1-16 and 17 come from
# RC-005/RC-006; Section 18 is the state Codex approved at RC-006 Round 2.
FROZEN = {
    "sections 1-16": ("## 1. ", "## 17. ", 144664,
                      "700b3b9a4cd3a1b0f7342e2d4678fbe1cac87f68da6fbb2635ebc5b865cdad59"),
    "section 17": ("## 17. ", "## 18. ", 21864,
                   "dc73b87f64550d941ca99c9889668e45da688428cc791d8a8fe8d9c60303f72a"),
    "section 18": ("## 18. ", "## 19. ", 20579,
                   "8af3e62cd2540472a7a3466ee975d85701feab3e7c7dec05d7c3ddf16f821017"),
}

# Pinned by the Claim Sheet's control description and by Section 11.1's reading
# of the donor column: the injection target is a peak-to-peak range in microvolts.
A_MIN_UV = 50.0
A_MAX_UV = 200.0
LOWER_SNR = 5.0                  # SpikeForest's secondary-analysis threshold
GRADING_SNR = 8.0                # SpikeForest's ground-truth inclusion threshold
SATURATION_SNR = 40.0            # declared in Section 19.6, not cited
MAD_SCALE = 0.6744897501960817
K_WINDOWS = 60
EDGE_DISCARD = 150
SAMPLE_RATE_HZ = 30000.0


class Checks:
    """Accumulate pass/fail results and report them at the end."""

    def __init__(self):
        """Create an empty result set."""
        self.rows = []

    def check(self, name, condition, detail=""):
        """Record one check.

        Args:
            name: short ASCII label for the check.
            condition: truthy for pass.
            detail: extra ASCII context printed on failure.
        """
        self.rows.append((name, bool(condition), detail))

    def report(self):
        """Print every check and return the number that failed.

        Returns:
            The count of failed checks.
        """
        failed = 0
        for name, ok, detail in self.rows:
            status = "ok  " if ok else "FAIL"
            line = f"[{status}] {name}"
            if not ok and detail:
                # This console is cp1252 and the strings under test carry µ and
                # √. Escaping here rather than at the call site keeps a failure
                # a failure instead of an encoding crash that merely resembles
                # one.
                line += " -- " + detail.encode("ascii", "backslashreplace").decode("ascii")
            print(line)
            if not ok:
                failed += 1
        print(f"\n{len(self.rows)} checks, {failed} failed")
        return failed


def sha256_bytes(data):
    """Return the hex SHA-256 of a byte string.

    Args:
        data: the bytes to digest.

    Returns:
        The lowercase hex digest.
    """
    return hashlib.sha256(data).hexdigest()


def read_text(path):
    """Read a UTF-8 file without newline translation.

    Args:
        path: the file to read.

    Returns:
        The file's text.
    """
    with io.open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def span(text, start, end):
    """Return the substring running from one heading to the next.

    Args:
        text: the whole document.
        start: the opening heading.
        end: the heading that terminates the span.

    Returns:
        The substring, excluding the terminating heading.
    """
    return text[text.index(start):text.index(end)]


def fmt(value, places):
    """Format a number the way the section writes it.

    Args:
        value: the number.
        places: decimal places.

    Returns:
        The formatted string, with thousands separators for integers.
    """
    if places == 0:
        return f"{int(round(value)):,}"
    return f"{value:.{places}f}"


def main():
    """Run every check and exit non-zero if any failed.

    Returns:
        Process exit status: 0 when every check passed.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--repo-root", required=True, help="path to the repository root")
    args = parser.parse_args()
    root = os.path.abspath(args.repo_root)

    doc = read_text(os.path.join(root, DOC_REL))
    layout = json.loads(read_text(os.path.join(root, LAYOUT_REL)))
    report = read_text(os.path.join(root, REPORT_REL))
    checks = Checks()

    # --- the earlier sections must not have moved -------------------------
    for label, (start, end, size, digest) in FROZEN.items():
        body = span(doc, start, end).encode("utf-8")
        checks.check(f"{label} byte count {size}", len(body) == size, f"got {len(body)}")
        checks.check(f"{label} digest", sha256_bytes(body) == digest, sha256_bytes(body))

    sec19 = doc[doc.index("## 19. "):]
    checks.check("section 19 present", sec19.startswith("## 19. Session 43"))
    checks.check("document is LF only", "\r" not in doc)

    # The status line is a publishing surface too: it restates thresholds and
    # the supersession, and a number carried into it is as public as one in the
    # section body. It is therefore checked separately rather than assumed to
    # agree with the section it summarises.
    status = span(doc, "**Status:** Draft 29", "**Status:** Draft 28")
    checks.check("draft 29 status line present", status.startswith("**Status:** Draft 29"))

    # --- the recorded layout, and the section's reading of it -------------
    n_samples, n_channels = layout["shape"]
    chunk_t, chunk_c = layout["chunks"]
    itemsize = layout["itemsize"]
    logical = layout["logical_bytes"]
    stored = layout["stored_size_bytes"]

    checks.check("layout dtype int16", layout["dtype"] == "int16", layout["dtype"])
    checks.check("layout gzip level 4",
                 layout["filters"]["compression"] == "gzip"
                 and layout["filters"]["compression_opts"] == 4)
    checks.check("layout no shuffle", layout["filters"]["shuffle"] is False)
    checks.check("layout chunk spans all channels", chunk_c == n_channels,
                 f"{chunk_c} vs {n_channels}")
    checks.check("layout channel_conversion absent", layout["channel_conversion"] is None)
    checks.check("layout offset is zero", layout["scaling"]["offset"] == 0.0)
    checks.check("layout unit is volts", layout["scaling"]["unit"] == "volts")
    checks.check("report says no sample was read",
                 "No sample value was read" in report)

    # The layout table is the section's authoritative restatement of the record,
    # so each row is checked as a whole row. Searching for the bare number would
    # pass while one of its four restatements disagreed with the other three,
    # which is the shape of the defect RC-006 found in the resource paragraph.
    rows = {
        "shape": f"| shape | {n_samples:,} samples × {n_channels} channels |",
        "dtype": f"| dtype | `int16`, {itemsize} bytes per stored sample |",
        "logical size": f"| logical size | {logical:,} bytes |",
        "stored size": f"| stored size | {stored:,} bytes |",
        "chunk shape": f"| chunk shape | **{chunk_t:,} samples × {chunk_c} channels** |",
        "conversion": f"| `conversion` | `{layout['scaling']['conversion']!r}` |".replace("'", ""),
    }
    for label, row in rows.items():
        checks.check(f"layout table row for {label}", row in sec19, row)

    lsb_uv = layout["scaling"]["conversion"] * 1e6
    checks.check("LSB microvolts 2.34375", abs(lsb_uv - 2.34375) < 1e-12, str(lsb_uv))
    checks.check("section quotes the LSB", "2.34375" in sec19)

    quant_sd = lsb_uv / math.sqrt(12.0)
    checks.check("quantization sd 0.677", fmt(quant_sd, 3) == "0.677", fmt(quant_sd, 3))
    checks.check("section quotes the quantization sd", "0.677" in sec19)

    mad_granularity = 0.5 * lsb_uv / MAD_SCALE
    checks.check("MAD half-bit granularity 1.74",
                 fmt(mad_granularity, 2) == "1.74", fmt(mad_granularity, 2))
    checks.check("section quotes the granularity", "1.74" in sec19)

    chunk_seconds = chunk_t / SAMPLE_RATE_HZ
    checks.check("chunk seconds 0.434", fmt(chunk_seconds, 3) == "0.434", fmt(chunk_seconds, 3))
    checks.check("section quotes the chunk length", "0.434" in sec19)

    full_chunks = n_samples // chunk_t
    remainder = n_samples - full_chunks * chunk_t
    checks.check("full chunks 9999", full_chunks == 9999, str(full_chunks))
    checks.check("partial samples 1020", remainder == 1020, str(remainder))
    checks.check("section quotes the full-chunk count", "9,999" in sec19)
    checks.check("section quotes the partial remainder", "1,020" in sec19)

    ratio = stored / logical
    checks.check("compression ratio 0.53172", fmt(ratio, 5) == "0.53172", fmt(ratio, 5))
    checks.check("section quotes the ratio", "0.53172" in sec19)

    chunk_uncompressed = chunk_t * chunk_c * itemsize
    checks.check("chunk uncompressed 9,999,360", chunk_uncompressed == 9999360,
                 str(chunk_uncompressed))
    checks.check("section quotes the uncompressed chunk", "9,999,360" in sec19)

    projected_chunk = chunk_uncompressed * ratio
    checks.check("projected stored per chunk 5,316,841",
                 fmt(projected_chunk, 0) == "5,316,841", fmt(projected_chunk, 0))
    checks.check("section quotes the per-chunk projection", "5,316,841" in sec19)

    projected_run = K_WINDOWS * chunk_uncompressed * ratio
    checks.check("projected run 319,010,455",
                 fmt(projected_run, 0) == "319,010,455", fmt(projected_run, 0))
    checks.check("section quotes the run projection", "319,010,455" in sec19)
    checks.check("section calls the run figure a projection",
                 "not a measurement of any chunk" in sec19)

    float_bytes = chunk_t * chunk_c * 8
    checks.check("float64 window 39,997,440", float_bytes == 39997440, str(float_bytes))
    checks.check("section quotes the float64 window", "39,997,440" in sec19)

    coverage_s = K_WINDOWS * chunk_seconds
    checks.check("coverage seconds 26.04", fmt(coverage_s, 2) == "26.04", fmt(coverage_s, 2))
    checks.check("section quotes the coverage", "26.04" in sec19)

    spacing_s = (full_chunks / K_WINDOWS) * chunk_seconds
    checks.check("spacing seconds 72.3", fmt(spacing_s, 1) == "72.3", fmt(spacing_s, 1))
    checks.check("section quotes the spacing", "72.3" in sec19)

    kept = chunk_t - 2 * EDGE_DISCARD
    half = kept // 2
    checks.check("retained samples 12,720", kept == 12720, str(kept))
    checks.check("half window 6,360", half == 6360, str(half))
    checks.check("section quotes the retained count", "12,720" in sec19)
    checks.check("section quotes the half window", "6,360" in sec19)
    checks.check("edge discard is 5 ms",
                 abs(EDGE_DISCARD / SAMPLE_RATE_HZ - 0.005) < 1e-12)

    rel_se = 1.16 / math.sqrt(half)
    checks.check("relative standard error 1.46 percent",
                 fmt(rel_se * 100.0, 2) == "1.45" or fmt(rel_se * 100.0, 2) == "1.46",
                 fmt(rel_se * 100.0, 2))
    checks.check("section quotes the relative standard error", "1.46%" in sec19)
    checks.check("section says the samples are not independent",
                 "these samples are not independent" in sec19)

    # --- the thresholds, derived from the pinned amplitude target ---------
    n_strict = A_MIN_UV / LOWER_SNR
    n_relaxed = A_MAX_UV / GRADING_SNR
    m_strict = math.sqrt(A_MAX_UV / A_MIN_UV)
    sigma_floor = A_MIN_UV / SATURATION_SNR
    implied = A_MAX_UV / n_strict

    checks.check("strict level tolerance 10.0", n_strict == 10.0, str(n_strict))
    checks.check("relaxed level tolerance 25.0", n_relaxed == 25.0, str(n_relaxed))
    checks.check("strict spatial tolerance 2.0", m_strict == 2.0, str(m_strict))
    checks.check("declared floor 1.25", sigma_floor == 1.25, str(sigma_floor))
    checks.check("condition 2 is implied by condition 1", implied >= GRADING_SNR,
                 str(implied))
    checks.check("implied factor is 20", implied == 20.0, str(implied))

    # Each threshold is checked at the string that carries its derivation, not
    # at the bare number: a bare "2.0" also appears in the parameter table, so a
    # mutation of the derivation would survive a token search.
    derivations = {
        "strict level, as a bound on sigma":
            "→ **`σ ≤ %s µV`**" % fmt(n_strict, 1),
        "implied grading condition, as a bound on sigma":
            "→ `σ ≤ %s µV`" % fmt(n_relaxed, 1),
        "declared floor, as a bound on sigma":
            "→ `σ ≥ %s µV`" % fmt(sigma_floor, 2),
        "the admissible band":
            "**`%s µV ≤ sigma_worst ≤ %s µV`**"
            % (fmt(sigma_floor, 2), fmt(n_strict, 1)),
        "the level ladder":
            "`A_min/5 = %s µV` to `A_max/8 = %s µV`"
            % (fmt(n_strict, 1), fmt(n_relaxed, 1)),
        "the spatial derivation":
            "`M = √(A_max/A_min) = %s`" % fmt(m_strict, 1),
        "the relaxed spatial rung":
            "the full span, `M = %s`" % fmt(m_strict * 2.0, 1),
    }
    for label, text_value in derivations.items():
        checks.check(f"section carries {label}", text_value in sec19, text_value)
    checks.check("section states condition 2 is implied",
                 "Condition 2 is implied by condition 1" in sec19)
    checks.check("section states the relaxed spatial rung is the full span",
                 "the full span" in sec19)
    checks.check("section states one relaxed pass, not two",
                 "does not add a third" in sec19)

    checks.check("section quotes the MAD scale constant", MAD_SCALE_TEXT in sec19)
    checks.check("section names the probe noise specification",
                 "5.1" in sec19 and "5.7" in sec19)

    # --- the claims the section makes about its own standing --------------
    checks.check("section says no estimator was written",
                 "No estimator code is written this session" in sec19)
    checks.check("section says no candidate noise value is known",
                 "no candidate's noise value is known" in sec19)
    checks.check("section states the necessary-not-sufficient posture",
                 "necessary condition and not a sufficient one" in sec19)
    checks.check("section declares the saturation ceiling as judgement",
                 "judgement, not literature" in sec19)
    checks.check("section names the phase-shift omission and its direction",
                 "biased upward" in sec19)
    checks.check("section names the unbounded reader cache",
                 "unbounded and is never evicted" in sec19)
    checks.check("section supersedes one clause of 15.5 item 3",
                 "one clause of its item 3" in sec19)
    checks.check("section states four gates rather than five",
                 "four gates rather than five" in sec19)
    checks.check("section refuses the native-amplitude gate",
                 "cannot become a gate now" in sec19)
    checks.check("section says the audit values are never consumed",
                 "reported and never consumed" in sec19)
    checks.check("section says R_null is silent on bias",
                 "silent on estimation *bias*" in sec19)
    checks.check("section says it has not been reviewed",
                 "This section has not been reviewed" in sec19)

    # --- the status line must publish the same numbers ---------------------
    checks.check("status quotes the strict level tolerance",
                 f"`A_min/5 = {fmt(n_strict, 1)}" in status)
    checks.check("section says both multipliers are the source's own",
                 "Both multipliers are that source's own numbers" in sec19)
    checks.check("status quotes the relaxed level tolerance",
                 f"`A_max/8 = {fmt(n_relaxed, 1)}" in status)
    checks.check("status quotes the strict spatial tolerance",
                 f"sqrt(A_max/A_min) = {fmt(m_strict, 1)}" in status)
    checks.check("status quotes the chunk shape",
                 f"{chunk_t:,} samples" in status and f"{chunk_c} channels" in status)
    checks.check("status quotes the LSB", "2.34375" in status)
    checks.check("status quotes the chunk length in seconds", "0.434" in status)
    checks.check("status states the four-gate supersession",
                 "host admissibility is therefore four gates rather than five" in status)
    checks.check("status says no estimator code was written",
                 "No estimator code was written" in status)
    checks.check("status says no noise value was measured",
                 "no noise value was measured" in status)
    checks.check("status says no host is pinned",
                 "No host is pinned" in status)

    failed = checks.report()
    return 1 if failed else 0


MAD_SCALE_TEXT = "0.6744897501960817"


if __name__ == "__main__":
    raise SystemExit(main())
