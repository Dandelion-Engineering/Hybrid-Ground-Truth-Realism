"""Re-derive every number Section 19 states, from the records rather than the prose.

Section 19 of ``agents/Claude/Tier A Host and Injection Zone Selection.md``
specifies the host noise gate. It is a contract rather than a result, so the
only executable property it has is that its arithmetic closes: every threshold
it publishes must follow from a pinned quantity, every layout figure must follow
from the recorded probe output, and every filter figure must follow from the
recorded filter-chain measurement rather than from a number someone typed.

This checker is read-only. It recomputes each figure from

  * ``raw_ap_layout_CSHL047_Probe01_2026-08-18.json`` -- the storage layout,
  * ``filter_chain_2026-08-18.json`` -- the preprocessing measurement,
  * ``Reproducibility Packet/results/host_timing_index.jsonl`` -- the measured
    sampling rates, and
  * the pinned 50-200 uV peak-to-peak injection amplitude target,

then requires the section to contain the recomputed value as written. It also
holds the earlier sections fixed: the same-state approved Sections 1-16, 17 and
18 spans must be byte-identical to the digests recorded when they were approved.

It carries negative checks as well as positive ones. A repaired document has to
stop saying the thing that was repaired, and a checker that only looks for the
new string goes green on a document containing both.

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
FILTER_REL = os.path.join("agents", "Claude", "tools", "filter_chain_2026-08-18.json")
TIMING_REL = os.path.join("Reproducibility Packet", "results", "host_timing_index.jsonl")

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
MAD_SCALE_TEXT = "0.6744897501960817"
MAD_SCALE = 0.6744897501960817
K_WINDOWS = 60
MARGIN_SAMPLES = 500
SAMPLE_RATE_HZ = 30000.0
CUTOFF_HZ = 300.0
SI_MARGIN_MULTIPLIER = 5.0       # SpikeInterface's margin_ms="auto" rule

# Strings Draft 29 carried that Draft 30 repaired, split by how they may
# survive. RETIRED_ABSENT must not appear anywhere in the section: they are
# stale numbers and formulas, and a document that still contains one is a
# document with two answers. RETIRED_QUOTED_ONLY may appear, but only inside
# the two subsections whose job is to record what was withdrawn -- quoting a
# retracted claim inside its own retraction is not the same as asserting it.
RETIRED_ABSENT = {
    "the brick-wall filter step": "in the frequency domain",
    "the old edge-discard width": "150 samples (5 ms)",
    "the old retained sample count": "12,720",
    "the old half-window count": "6,360",
    "the old grid formula": "floor(k · C / K)",
    "the old window spacing": "72.3 s",
    "the unreviewed claim": "This section has not been reviewed",
    "the identical-by-construction claim": "the *true* per-channel scale is the same for both",
    "the blanket necessity claim": "every bound below is consequently",
    "the superseded clause of 15.5": "one clause of its item 3",
}
RETIRED_QUOTED_ONLY = {
    "the four-gate supersession": "four gates rather than five",
    "the stale relaxation restatement": "`12.5 → 25.0",
}


# How many times each value is restated inside Section 19. A number restated
# four times and mutated once still appears, so a substring search passes while
# one restatement disagrees with its siblings -- the defect shape RC-006 found
# in Section 18.2 and the reason the layout table is checked by whole rows. The
# census catches the same shape for values that are not in a table. A deliberate
# edit that changes a count updates this table; an accidental one goes red.
RESTATEMENTS = {
    "74.214": 5,          # the guaranteed-detection duration
    "12,020": 3,          # retained samples after the margin
    "6,010": 4,           # the split-half length
    "16.667": 3,          # the margin in milliseconds
    "500 samples": 3,     # the margin in samples
    "padlen=18": 3,       # the pinned scipy padding length
    "13,020": 5,          # the chunk length in samples
    "9,999": 4,           # whole chunks inside the extent
    "2.34375": 2,         # the least significant bit in microvolts
    "9,999,360": 2,       # the uncompressed chunk in bytes
    "26.04": 2,           # the sampled coverage in seconds
}


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
            line = "[%s] %s" % (status, name)
            if not ok and detail:
                # This console is cp1252 and the strings under test carry mu and
                # the radical sign. Escaping here rather than at the call site
                # keeps a failure a failure instead of an encoding crash that
                # merely resembles one.
                line += " -- " + detail.encode("ascii", "backslashreplace").decode("ascii")
            print(line)
            if not ok:
                failed += 1
        print("\n%d checks, %d failed" % (len(self.rows), failed))
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
    """Return the substring running from one marker to the next.

    Args:
        text: the whole document.
        start: the opening marker.
        end: the marker that terminates the span.

    Returns:
        The substring, excluding the terminating marker.
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
        return "{:,}".format(int(round(value)))
    return "{:.{}f}".format(value, places)


def grid_indices(n_chunks, k_windows):
    """Return Section 19.4's window grid.

    Args:
        n_chunks: C, the number of whole chunks inside the AP extent.
        k_windows: K, the number of windows.

    Returns:
        The list of chunk indices, using the section's explicit
        floor(x + 0.5) rather than a language's rounding rule.
    """
    return [int(math.floor(k * (n_chunks - 1) / (k_windows - 1) + 0.5))
            for k in range(k_windows)]


def max_rate_deviation(path):
    """Return the largest relative departure from the nominal rate.

    Args:
        path: the host timing index, one JSON record per line.

    Returns:
        A (deviation, n_series) pair, where deviation is the largest
        |rate/nominal - 1| across every AP series in the index.
    """
    worst = 0.0
    count = 0
    with io.open(path, "r", encoding="utf-8", newline="") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            for series in record["series"]:
                count += 1
                worst = max(worst, abs(series["rate_hz"] / SAMPLE_RATE_HZ - 1.0))
    return worst, count


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
    filt = json.loads(read_text(os.path.join(root, FILTER_REL)))
    checks = Checks()

    # --- the earlier sections must not have moved -------------------------
    for label, (start, end, size, digest) in FROZEN.items():
        body = span(doc, start, end).encode("utf-8")
        checks.check("%s byte count %d" % (label, size), len(body) == size,
                     str(len(body)))
        checks.check("%s digest" % label, sha256_bytes(body) == digest,
                     sha256_bytes(body))

    sec19 = doc[doc.index("## 19. "):]
    checks.check("section 19 present", sec19.startswith("## 19. Session 43"))
    checks.check("document is LF only", "\r" not in doc)

    # The status line is a publishing surface too: it restates thresholds and
    # findings, and a number carried into it is as public as one in the section
    # body. It is therefore checked separately rather than assumed to agree with
    # the section it summarises.
    status = span(doc, "**Status:** Draft 30", "**Status:** Draft 29")
    checks.check("draft 30 status line present", status.startswith("**Status:** Draft 30"))
    checks.check("draft 29 status line retained below it",
                 "**Status:** Draft 29 — Claude Session 43" in doc)
    checks.check("draft 30 status line hands off to draft 29",
                 status.rstrip().endswith("Draft 29's own status line follows."))

    # --- strings the repair had to remove ---------------------------------
    # The two subsections that record the withdrawal. Anything quoted from
    # draft 29 has to live inside one of them.
    withdrawal = sec19[sec19.index("### 19.8 "):sec19.index("### 19.9 ")]         + sec19[sec19.index("### 19.11 "):]
    for label, text_value in RETIRED_ABSENT.items():
        checks.check("draft 29's %s is gone from the section" % label,
                     text_value not in sec19, text_value)
        checks.check("draft 29's %s is gone from the status line" % label,
                     text_value not in status, text_value)
    for label, text_value in RETIRED_QUOTED_ONLY.items():
        checks.check("draft 29's %s survives only inside the withdrawal record" % label,
                     sec19.count(text_value) == withdrawal.count(text_value)
                     and withdrawal.count(text_value) > 0,
                     "%d in section, %d in the withdrawal record"
                     % (sec19.count(text_value), withdrawal.count(text_value)))
        checks.check("draft 29's %s is not asserted in the status line" % label,
                     text_value not in status, text_value)

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
                 "%d vs %d" % (chunk_c, n_channels))
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
        "shape": "| shape | {:,} samples × {} channels |".format(n_samples, n_channels),
        "dtype": "| dtype | `int16`, {} bytes per stored sample |".format(itemsize),
        "logical size": "| logical size | {:,} bytes |".format(logical),
        "stored size": "| stored size | {:,} bytes |".format(stored),
        "chunk shape": "| chunk shape | **{:,} samples × {} channels** |".format(chunk_t, chunk_c),
        "conversion": "| `conversion` | `{!r}` |".format(layout["scaling"]["conversion"]).replace("'", ""),
    }
    for label, row in rows.items():
        checks.check("layout table row for %s" % label, row in sec19, row)

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

    # --- the window grid, and the coverage it licenses ---------------------
    indices = grid_indices(full_chunks, K_WINDOWS)
    gaps = [indices[i + 1] - indices[i] for i in range(K_WINDOWS - 1)]
    gap = max(gaps)
    checks.check("grid has K distinct indices", len(set(indices)) == K_WINDOWS,
                 str(len(set(indices))))
    checks.check("grid is strictly increasing", min(gaps) > 0, str(min(gaps)))
    checks.check("grid starts at chunk 0", indices[0] == 0, str(indices[0]))
    checks.check("grid ends at the last full chunk", indices[-1] == full_chunks - 1,
                 str(indices[-1]))
    checks.check("largest grid gap is 170", gap == 170, str(gap))
    checks.check("section quotes the gap", "`g = 170` chunks" in sec19)
    checks.check("section quotes the first grid indices",
                 "`0, 169, 339, …, 9,829, 9,998`" in sec19)

    guaranteed_s = (gap + 1) * chunk_seconds
    checks.check("guaranteed-detection duration 74.214",
                 fmt(guaranteed_s, 3) == "74.214", fmt(guaranteed_s, 3))
    checks.check("section quotes the guaranteed duration", "74.214 s" in sec19)
    checks.check("section states the unsampled-run length",
                 "`g − 1 = 169`" in sec19)
    checks.check("section states what the grid cannot see",
                 "is invisible to every quantity in this section" in sec19)

    coverage_s = K_WINDOWS * chunk_seconds
    checks.check("coverage seconds 26.04", fmt(coverage_s, 2) == "26.04", fmt(coverage_s, 2))
    checks.check("section quotes the coverage", "26.04" in sec19)
    coverage_pct = 100.0 * K_WINDOWS / full_chunks
    checks.check("coverage fraction 0.600 percent",
                 fmt(coverage_pct, 3) == "0.600", fmt(coverage_pct, 3))
    checks.check("section quotes the coverage fraction", "**0.600%**" in sec19)

    # --- the preprocessing chain, from the filter-chain record -------------
    checks.check("filter record is the 13,020-sample window",
                 filt["window_samples"] == chunk_t, str(filt["window_samples"]))
    checks.check("filter record cutoff is 300 Hz",
                 filt["cutoff_hz"] == CUTOFF_HZ, str(filt["cutoff_hz"]))
    checks.check("filter order is 5", filt["butterworth"]["order"] == 5,
                 str(filt["butterworth"]["order"]))
    checks.check("filter has three second-order sections",
                 filt["butterworth"]["sections"] == 3,
                 str(filt["butterworth"]["sections"]))

    impulse = filt["impulse"]
    checks.check("DFT high-pass impulse at the centre equals -1/n",
                 impulse["matches_closed_form"] is True,
                 str(impulse["h_centre"]))
    checks.check("DFT high-pass is not confined to the discarded edges",
                 impulse["max_abs_h_outside_150_sample_edges"] > 0.0,
                 str(impulse["max_abs_h_outside_150_sample_edges"]))
    checks.check("section quotes the closed-form impulse value",
                 "`−1/13020`" in sec19)

    radius = filt["butterworth"]["max_pole_radius"]
    tau = filt["butterworth"]["tau_samples"]
    checks.check("section quotes the pole radius",
                 "`%s`" % fmt(radius, 9) in sec19, fmt(radius, 9))
    checks.check("section quotes the time constant in samples",
                 "**%s samples" % fmt(tau, 3) in sec19, fmt(tau, 3))
    checks.check("section quotes the time constant in milliseconds",
                 "(%s ms)**" % fmt(1000.0 * tau / SAMPLE_RATE_HZ, 3) in sec19,
                 fmt(1000.0 * tau / SAMPLE_RATE_HZ, 3))
    margins_in_tau = MARGIN_SAMPLES / tau
    checks.check("margin is 9.703 time constants",
                 fmt(margins_in_tau, 3) == "9.703", fmt(margins_in_tau, 3))
    checks.check("section quotes the margin in time constants",
                 "**%s time constants**" % fmt(margins_in_tau, 3) in sec19,
                 fmt(margins_in_tau, 3))
    residual = math.exp(-margins_in_tau)
    checks.check("residual factor 6.1e-05",
                 "%.1e" % residual == "6.1e-05", "%.1e" % residual)
    checks.check("section quotes the residual factor", "`6.1e-05`" in sec19)

    # The isolated-window study is what licenses the margin, so the section's
    # four reported figures are read back out of the record it came from rather
    # than trusted as prose.
    si_margin_ms = SI_MARGIN_MULTIPLIER * (1000.0 / CUTOFF_HZ)
    study = {(r["construction"], r["margin_samples"]): r for r in filt["margin_study"]
             if r["excursion_uv"] == 0.0}
    brick_150 = study[("dft_brickwall", 150)]["worst_relative_sigma_error"]
    brick_500 = study[("dft_brickwall", 500)]["worst_relative_sigma_error"]
    butter_500 = study[("butterworth_sosfiltfilt", 500)]["worst_relative_sigma_error"]
    butter_sample = study[("butterworth_sosfiltfilt", 500)]["worst_max_abs_sample_error_uv"]
    checks.check("brick wall does not improve with a wider margin",
                 abs(brick_500) > 0.5 * abs(brick_150),
                 "%r vs %r" % (brick_500, brick_150))
    checks.check("butterworth at 500 beats the brick wall by >=1000x",
                 abs(butter_500) * 1000.0 <= abs(brick_500),
                 "%r vs %r" % (butter_500, brick_500))
    checks.check("section quotes the brick wall error at 150 samples",
                 "`+%s%%` at 150 samples" % fmt(100.0 * brick_150, 3) in sec19,
                 fmt(100.0 * brick_150, 3))
    checks.check("section quotes the brick wall error at 500 samples",
                 "`+%s%%` at 500" % fmt(100.0 * brick_500, 3) in sec19,
                 fmt(100.0 * brick_500, 3))
    checks.check("section quotes the brick wall error to two places",
                 "**`+%s%%`**" % fmt(100.0 * brick_150, 2) in sec19,
                 fmt(100.0 * brick_150, 2))
    checks.check("section quotes the butterworth sample error",
                 "%s µV**" % fmt(butter_sample, 4) in sec19, fmt(butter_sample, 4))

    checks.check("SpikeInterface auto margin is 16.667 ms",
                 fmt(si_margin_ms, 3) == "16.667", fmt(si_margin_ms, 3))
    checks.check("auto margin is 500 samples at 30 kHz",
                 round(si_margin_ms * SAMPLE_RATE_HZ / 1000.0) == MARGIN_SAMPLES,
                 str(si_margin_ms * SAMPLE_RATE_HZ / 1000.0))
    checks.check("section quotes the margin in samples and milliseconds",
                 "**500 samples (16.667 ms)**" in sec19)
    checks.check("section names the SpikeInterface margin rule",
                 "`5 × (1000 / freq_min)`" in sec19)
    checks.check("section names the filter defaults it inherits",
                 "`filter_order=5`" in sec19 and "`ftype=\"butter\"`" in sec19
                 and "`direction=\"forward-backward\"`" in sec19)
    checks.check("section pins padlen by value in the chain step",
                 "`padlen=18` is scipy's own default for this particular `sos`" in sec19)
    # Both parameter-table rows are checked as whole rows rather than by token,
    # for the reason RC-006 established: a restatement can disagree with its
    # siblings while every individual number still appears somewhere.
    checks.check("parameter table carries the windows row",
                 "| windows | `K = %d`, at chunk indices "
                 "`floor(k·(C−1)/(K−1) + 0.5)` |" % K_WINDOWS in sec19)
    checks.check("parameter table carries the high-pass row",
                 "| high-pass | fifth-order Butterworth at %d Hz, `sos`, "
                 "forward–backward via `sosfiltfilt`, `padtype=\"odd\"`, "
                 "`padlen=18` |" % int(CUTOFF_HZ) in sec19)
    checks.check("parameter table carries the margin row",
                 "| margin | %d samples (%s ms) at each end, after the filter |"
                 % (MARGIN_SAMPLES, fmt(si_margin_ms, 3)) in sec19)
    checks.check("section names sosfiltfilt", "`scipy.signal.sosfiltfilt`" in sec19)
    checks.check("section says the anchor filter is zero phase", "zero phase" in sec19)

    kept = chunk_t - 2 * MARGIN_SAMPLES
    half = kept // 2
    checks.check("retained samples 12,020", kept == 12020, str(kept))
    checks.check("half window 6,010", half == 6010, str(half))
    checks.check("section quotes the retained count", "**12,020**" in sec19)
    checks.check("section quotes the half window", "6,010" in sec19)

    rel_se = 1.16 / math.sqrt(half)
    checks.check("relative standard error 1.50 percent",
                 fmt(rel_se * 100.0, 2) == "1.50", fmt(rel_se * 100.0, 2))
    checks.check("section quotes the relative standard error", "**1.50%**" in sec19)
    checks.check("section says the samples are not independent",
                 "these samples are not independent" in sec19)

    rate_dev, n_series = max_rate_deviation(os.path.join(root, TIMING_REL))
    checks.check("timing index holds 21 series", n_series == 21, str(n_series))
    checks.check("largest rate deviation 9.946e-06",
                 "%.3e" % rate_dev == "9.946e-06", "%.3e" % rate_dev)
    checks.check("section quotes the rate deviation", "`9.946e-06`" in sec19)
    corner_shift = CUTOFF_HZ * rate_dev
    checks.check("corner shift 0.003 Hz",
                 fmt(corner_shift, 3) == "0.003", fmt(corner_shift, 3))
    checks.check("section quotes the corner shift", "**0.003 Hz**" in sec19)

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
    checks.check("probe spec noise is four times the floor",
                 abs(5.1 / sigma_floor - 4.08) < 0.01, str(5.1 / sigma_floor))
    checks.check("section quotes the MAD scale constant", MAD_SCALE_TEXT in sec19)
    checks.check("section names the probe noise specification",
                 "5.1" in sec19 and "5.7" in sec19)

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
            "**`%s µV ≤ sigma_worst_sampled ≤ N`**" % fmt(sigma_floor, 2),
        "the level ladder":
            "`A_min/5 = %s µV` to `A_max/8 = %s µV`"
            % (fmt(n_strict, 1), fmt(n_relaxed, 1)),
        "the relaxed pass restatement":
            "`%s → %s µV`" % (fmt(n_strict, 1), fmt(n_relaxed, 1)),
        "the spatial derivation":
            "`M = √(A_max/A_min) = %s`" % fmt(m_strict, 1),
        "the relaxed spatial rung":
            "the full span, `M = %s`" % fmt(m_strict * 2.0, 1),
        "the pass rule's own band":
            "**`%s µV ≤ sigma_worst_sampled ≤ N`**" % fmt(sigma_floor, 2),
    }
    for label, text_value in derivations.items():
        checks.check("section carries %s" % label, text_value in sec19, text_value)
    checks.check("section states condition 2 is implied",
                 "Condition 2 is implied by condition 1" in sec19)
    checks.check("section states one relaxed pass, not two",
                 "does not add a third" in sec19)
    checks.check("section says the floor does not relax",
                 "**The floor does not relax.**" in sec19)
    checks.check("parameter table carries the floor row",
                 "| **level floor** | **%s µV, strict and relaxed alike** |"
                 % fmt(sigma_floor, 2) in sec19)

    # --- the pass rule's branches -----------------------------------------
    for label, text_value in {
        "branch 1, too loud": "1. **Level, too loud.**",
        "branch 2, too quiet": "2. **Level, too quiet.**",
        "branch 3, homogeneity": "3. **Homogeneity.**",
        "branch 4, resolution": "4. **Resolution.**",
        "the branches are ordered": "the first that fires is the disposition",
        "the too-quiet label": "`implausibly quiet`",
        "the homogeneity labels": "`resolved heterogeneity`",
        "the resolution branch is conditional":
            "`R_space_sampled ≤ M` and `R_null_sampled > M`",
    }.items():
        checks.check("section carries %s" % label, text_value in sec19, text_value)

    checks.check("section defines the degenerate-channel case",
                 "a channel literally constant across the retained core" in sec19)
    checks.check("section says degenerate channels are not masked",
                 "**counted and published, never masked**" in sec19)
    checks.check("section says no undefined ratio reaches a comparison",
                 "No undefined ratio enters a comparison." in sec19)
    checks.check("section separates input errors from unmeasurable rejections",
                 "**Input errors are not gate outcomes" in sec19)
    checks.check("section says an input error stops the order",
                 "the pinned order does not advance past it" in sec19)
    checks.check("section says an unmeasurable rejection advances the order",
                 "*is* a rejection and *does* advance the order" in sec19)

    # --- the percentile rule ----------------------------------------------
    n_band = 72
    p10_rank = math.ceil(0.10 * n_band)
    p90_rank = math.ceil(0.90 * n_band)
    checks.check("p10 rank at 72 channels is 8", p10_rank == 8, str(p10_rank))
    checks.check("p90 rank at 72 channels is 65", p90_rank == 65, str(p90_rank))
    checks.check("section quotes both percentile ranks",
                 "ranks **%d** and **%d**" % (p10_rank, p90_rank) in sec19)
    checks.check("section gives the percentile formula",
                 "`ceil(0.10 · n)`" in sec19 and "`ceil(0.90 · n)`" in sec19)

    # --- the convention direction, split by kind of bound -----------------
    checks.check("section states the floor substitution is weaker",
                 "is the **weaker** requirement" in sec19)
    checks.check("section states the ceiling substitution is stronger",
                 "is the **stronger** requirement" in sec19)
    checks.check("section carries the reviewer's counterexample",
                 "whose peak is `30σ` and whose trough is `−20σ`" in sec19)
    checks.check("section calls the floors necessary not sufficient",
                 "each is a necessary condition and not a sufficient one" in sec19)
    checks.check("section calls the ceiling sufficient not necessary",
                 "it is sufficient and not necessary" in sec19)

    # --- the claims the section makes about its own standing --------------
    for label, text_value in {
        "no estimator was written": "No estimator code is written this session",
        "no candidate noise value is known": "no candidate's noise value is known",
        "the saturation ceiling is judgement": "judgement, not literature",
        "the phase-shift omission and its direction": "biased upward",
        "the unbounded reader cache": "unbounded and is never evicted",
        "the withdrawal of the supersession": "**Consequence for §15.5: none.**",
        "five gates stand": "the five gates stand as written",
        "the native-amplitude refusal": "cannot become a gate now",
        "the audit values are never consumed": "reported and never consumed",
        "R_null is silent on bias": "silent on estimation *bias*",
        "the section has been reviewed once": "This section has been reviewed once",
        "the scipy pin": "`scipy==1.18.0`",
        "numpy did not move": "without moving `numpy` from `2.5.2`",
        "the sampled-grid boundary": "not over the recording",
        "both multipliers are the source's own":
            "Both multipliers are that source's own numbers",
        "the round 1 record": "### 19.11 Draft 30",
    }.items():
        checks.check("section states %s" % label, text_value in sec19, text_value)

    # --- the status line must publish the same numbers ---------------------
    for label, text_value in {
        "the strict level tolerance": "`10.0 → 25.0 µV`",
        "the withdrawal": "host admissibility is\nfive gates",
        "the renamed quantities": "`sigma_worst_sampled`",
        "the new grid formula": "`floor(k(C-1)/(K-1) + 0.5)`",
        "the guaranteed duration": "**74.214 s**",
        "the margin": "**500 samples (16.667 ms)**",
        "the closed-form impulse": "`-1/13020`",
        "the brick wall error": "+1.14%",
        "the butterworth error": "**+1e-06**",
        "no host is pinned": "No host is pinned",
        "no estimator was written": "no estimator was written",
        "the scipy pin": "`scipy==1.18.0`",
    }.items():
        checks.check("status line carries %s" % label,
                     text_value.replace("\n", " ") in " ".join(status.split()),
                     text_value)

    # --- every restatement of a value must agree with its siblings --------
    for value, expected in RESTATEMENTS.items():
        actual = sec19.count(value)
        checks.check("section restates %s exactly %d times" % (value, expected),
                     actual == expected, "found %d" % actual)

    failed = checks.report()
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
