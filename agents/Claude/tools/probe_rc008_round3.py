"""Evidence probe for Draft 34 of section 19 - the RC-008 Round-3 response.

Every number Draft 34 publishes about RC-008's Round-2 findings is computed
here rather than copied from the reviewer's message. Nothing in this file
reads the archive, the network or any project record other than the timing
index; the constructions are synthetic and each is built from numpy and scipy
directly.

  1. F6-R2, ground 1. Draft 33 kept the contiguous split partly on the claim
     that two adjacent stretches of a signal band-limited above 300 Hz give
     "close to independent" estimates. That is refuted, and not by one
     frequency: every f = m * fs / 6510 with m >= 66 lies above 300 Hz and
     repeats EXACTLY across the two 6,510-sample halves, so the halves are
     bit-identical and the two estimates are perfectly correlated. The
     reviewer's 400.921659 Hz is m = 87; the lowest member of the family is
     m = 66.
  2. F6-R2, ground 3. Draft 33 called it decisive that the decision rule
     cannot "cash" a lower R_null_sampled. The four branches say otherwise:
     with the level in band, R_space_sampled = 1.5 and M = 2.0, a contiguous
     R_null_sampled of 1 reaches `passes` and an interleaved one of 4 reaches
     branch 4 and `unmeasurable`.
  3. The reach of the split rule, proved over the whole truth table rather
     than exhibited on one fixture: the split enters the decision only through
     R_null_sampled, and R_null_sampled can move `passes` and `unmeasurable`
     into one another and relabel a homogeneity failure, and can do nothing
     else.
  4. The parity construction reproduced, with R_space_sampled held fixed
     across the two split rules.
  5. T7-R2: rank 1's raw AP series declares no rate, so "the candidate's own
     declared rate" names nothing on this candidate.

Usage:

    ./venv/Scripts/python.exe agents/Claude/tools/probe_rc008_round3.py \
        --repo-root . --out <path> [--records <path>]
"""

import argparse
import io
import json
import os
import sys

import numpy as np
from scipy import signal

FS_NOMINAL = 30000.0
RETAINED = 13020
HALF = RETAINED // 2
MAD_SCALE = 0.6744897501960817
TIMING_REL = os.path.join("Reproducibility Packet", "results",
                          "host_timing_index.jsonl")
RANK1_SESSION = "b52182e7-39f6-4914-9717-136db589706e"
RANK1_SERIES = "ElectricalSeriesProbe01AP"


class Checks(object):
    """Collect pass/fail lines and print them in the project's console form."""

    def __init__(self):
        self.lines = []
        self.failed = 0

    def heading(self, text):
        self.lines.append("")
        self.lines.append(text)

    def check(self, name, ok, detail=""):
        """Record one check; `detail` is printed either way."""
        if not ok:
            self.failed += 1
        self.lines.append("%s  %s%s" % ("PASS" if ok else "FAIL", name,
                                        ("  [%s]" % detail) if detail else ""))
        return ok

    def render(self):
        body = "\n".join(self.lines)
        total = sum(1 for line in self.lines
                    if line.startswith("PASS") or line.startswith("FAIL"))
        return "%s\n\nSummary\n%d checks, %d failed\n" % (body, total,
                                                          self.failed)


def sigma_hat(x, axis=-1):
    """MAD scale estimate along `axis`, the section 19.3 estimator."""
    med = np.median(x, axis=axis, keepdims=True)
    return np.median(np.abs(x - med), axis=axis) / MAD_SCALE


def nearest_rank(values, q):
    """Nearest-rank percentile: rank ceil(q * n) over ascending values."""
    ordered = np.sort(np.asarray(values, dtype=float))
    n = ordered.size
    rank = int(np.ceil(q * n))
    return ordered[max(rank, 1) - 1]


def spread(values):
    """The p90/p10 nearest-rank ratio section 19.4 fixes."""
    return nearest_rank(values, 0.90) / nearest_rank(values, 0.10)


def disposition(sigma_worst, sigma_quiet, r_space, r_null, n_tol, m_tol,
                floor=1.25):
    """Section 19.6's four ordered branches; the first that fires wins."""
    if sigma_worst > n_tol:
        return "fails-level-loud"
    if sigma_quiet < floor:
        return "fails-level-quiet"
    if r_space > m_tol:
        return ("fails-homogeneity-resolved" if r_space > r_null
                else "fails-homogeneity-resolution-limited")
    if r_null > m_tol:
        return "unmeasurable"
    return "passes"


def repeating_family(fs, half, f_min_hz):
    """Frequencies whose period divides `half` samples exactly, above f_min."""
    m_min = int(np.floor(f_min_hz * half / fs)) + 1
    return m_min, m_min * fs / half


def ground_one(c, records):
    """F6-R2: adjacent halves of an in-band signal need not be independent."""
    c.heading("1. F6-R2 ground 1  in-band does not imply near-independent")
    m_min, f_min = repeating_family(FS_NOMINAL, HALF, 300.0)
    c.check("the lowest in-band frequency whose period divides one half",
            m_min == 66 and abs(f_min - 304.1474654377880) < 1e-9,
            "m=%d f=%.10f Hz" % (m_min, f_min))
    f_codex = 87 * FS_NOMINAL / HALF
    c.check("the reviewer's frequency is a member of that family",
            abs(f_codex - 400.921659) < 5e-7, "m=87 f=%.9f Hz" % f_codex)

    # f = m * fs / HALF makes the phase at sample k exactly 2*pi*m*k/HALF, so
    # k and k + HALF carry the same phase. Evaluating it in that form rather
    # than as f * k / fs is the same function without the avoidable rounding,
    # which is what makes the identity exact in floating point as well.
    k = np.arange(RETAINED)
    exact = []
    for m in range(m_min, m_min + 135):
        x = np.sin(2.0 * np.pi * m * (k % HALF) / HALF)
        if np.max(np.abs(x[:HALF] - x[HALF:])) == 0.0:
            exact.append(m)
    c.check("every member tested repeats bit-identically across the halves",
            len(exact) == 135, "%d of 135 members exact" % len(exact))

    x = np.sin(2.0 * np.pi * 87 * (k % HALF) / HALF)
    a, b = x[:HALF], x[HALF:]
    c.check("the two halves are bit-identical at m=87",
            np.max(np.abs(a - b)) == 0.0,
            "max |A-B| = %.3e" % np.max(np.abs(a - b)))
    corr = float(np.corrcoef(a, b)[0, 1])
    c.check("their correlation is 1, not 'close to independent'",
            abs(corr - 1.0) < 1e-12, "corr = %.12f" % corr)
    ra = float(sigma_hat(a) / sigma_hat(b))
    c.check("the half-estimates agree exactly, so r_c is exactly 1",
            ra == 1.0, "r_c = %.15f" % ra)

    # A diagnostic, not a bound: the pinned high-pass does not destroy the
    # repetition, so the counterexample is not an artifact of skipping 19.3.
    sos = signal.butter(5, 300.0, btype="highpass", fs=FS_NOMINAL,
                        output="sos")
    block = np.sin(2.0 * np.pi * f_codex * (np.arange(RETAINED + 1000)
                                            - 500) / FS_NOMINAL)
    core = signal.sosfiltfilt(sos, block, padtype="odd", padlen=18)[500:-500]
    delta = float(np.max(np.abs(core[:HALF] - core[HALF:])))
    ratio = float(sigma_hat(core[:HALF]) / sigma_hat(core[HALF:]))
    c.check("after the pinned chain the halves still agree to r_c ~ 1",
            abs(ratio - 1.0) < 1e-6, "r_c = %.12f, max |A-B| = %.3e"
            % (ratio, delta))
    records["ground_one"] = {"m_min": m_min, "f_min_hz": f_min,
                             "f_reviewer_hz": f_codex,
                             "members_exact": len(exact),
                             "correlation": corr,
                             "post_filter_r_c": ratio,
                             "post_filter_max_half_delta": delta}


def ground_three(c, records):
    """F6-R2: the split difference has a decision destination."""
    c.heading("2. F6-R2 ground 3  the decision rule can cash the difference")
    n_tol, m_tol = 10.0, 2.0
    common = dict(sigma_worst=6.0, sigma_quiet=5.0, r_space=1.5,
                  n_tol=n_tol, m_tol=m_tol)
    contiguous = disposition(r_null=1.0, **common)
    interleaved = disposition(r_null=4.0, **common)
    c.check("the contiguous split reaches a pass", contiguous == "passes",
            contiguous)
    c.check("the interleaved split reaches branch 4",
            interleaved == "unmeasurable", interleaved)
    c.check("so the split difference changes the disposition",
            contiguous != interleaved,
            "%s -> %s" % (contiguous, interleaved))
    records["ground_three"] = {"contiguous": contiguous,
                               "interleaved": interleaved,
                               "r_space": 1.5, "M": m_tol}


def reach(c, records):
    """The split rule's whole reach, over the truth table rather than a case."""
    c.heading("3. The reach of the split rule, exhaustively")
    n_tol, m_tol, floor = 10.0, 2.0, 1.25
    worsts = [6.0, 12.0]
    quiets = [1.0, 5.0]
    spaces = [1.5, 3.0]
    nulls_low = [0.5, 1.0, 1.9]
    nulls_high = [2.1, 4.0, np.inf]
    moved, unchanged, relabelled = 0, 0, 0
    illegal = []
    for w in worsts:
        for q in quiets:
            for s in spaces:
                for lo in nulls_low:
                    for hi in nulls_high:
                        a = disposition(w, q, s, lo, n_tol, m_tol, floor)
                        b = disposition(w, q, s, hi, n_tol, m_tol, floor)
                        if a == b:
                            unchanged += 1
                            continue
                        pair = tuple(sorted((a, b)))
                        if pair == ("passes", "unmeasurable"):
                            moved += 1
                        elif pair == ("fails-homogeneity-resolution-limited",
                                      "fails-homogeneity-resolved"):
                            relabelled += 1
                        else:
                            illegal.append(pair)
    c.check("no move across the null boundary leaves the two failure classes",
            not illegal, "%d illegal transitions" % len(illegal))
    c.check("the only disposition change is pass <-> unmeasurable",
            moved == 9, "%d of %d state pairs" % (moved, moved + unchanged
                                                  + relabelled))
    c.check("the only other change is branch 3's label", relabelled == 6,
            "%d relabellings" % relabelled)
    c.check("every other state pair is untouched by the null",
            unchanged == 57, "%d unchanged" % unchanged)
    c.check("a level failure is never moved by the null",
            all(disposition(12.0, 5.0, 1.5, x, n_tol, m_tol, floor)
                == "fails-level-loud" for x in nulls_low + nulls_high))
    c.check("a quiet failure is never moved by the null",
            all(disposition(6.0, 1.0, 1.5, x, n_tol, m_tol, floor)
                == "fails-level-quiet" for x in nulls_low + nulls_high))
    c.check("a homogeneity failure is never converted to a non-failure",
            all(disposition(6.0, 5.0, 3.0, x, n_tol, m_tol, floor).startswith(
                "fails-homogeneity") for x in nulls_low + nulls_high))
    records["reach"] = {"moved": moved, "relabelled": relabelled,
                        "unchanged": unchanged, "illegal": len(illegal)}


def parity_core(ratios, base):
    """A deterministic 72 x 13,020 core whose two sample parities differ.

    ``ratios[c]`` is channel c's even-to-odd scale ratio and ``base[c]`` scales
    the whole row. Magnitudes are constant inside a parity class and the signs
    are balanced, so every MAD below is exact rather than sampled, and ``base``
    cancels out of the half-ratio r_c while it does move sigma_hat.
    """
    t = np.arange(RETAINED)
    sign = np.where((t % 4 == 0) | (t % 4 == 3), 1.0, -1.0)
    rows = []
    for ratio, scale in zip(ratios, base):
        even = float(ratio) if ratio >= 1 else 1.0
        odd = 1.0 if ratio >= 1 else 1.0 / float(ratio)
        rows.append(scale * np.where(t % 2 == 0, even, odd) * sign)
    return np.array(rows)


def parity(c, records):
    """The parity construction, and the two things the split cannot touch."""
    c.heading("4. The parity construction, and what the split does not reach")
    ratios = [2.0] * 8 + [1.0] * 56 + [0.5] * 8

    core = parity_core(ratios, [1.0] * 72)
    cont = spread(sigma_hat(core[:, :HALF]) / sigma_hat(core[:, HALF:]))
    inter = spread(sigma_hat(core[:, 0::2]) / sigma_hat(core[:, 1::2]))
    r_space = spread(sigma_hat(core))
    c.check("contiguous halves give exactly 1", abs(cont - 1.0) < 1e-12,
            "R_null = %.12f" % cont)
    c.check("even/odd interleaving gives exactly 4", abs(inter - 4.0) < 1e-12,
            "R_null = %.12f" % inter)
    c.check("interleaving expands, from inside strict M to outside it",
            cont < 2.0 < inter, "%.4f -> %.4f" % (cont, inter))

    # Both split rules partition the SAME retained core, which is the reason
    # R_space_sampled cannot see the choice: it is computed on that core.
    partitions = {
        "contiguous": np.concatenate([core[:, :HALF], core[:, HALF:]], axis=1),
        "interleaved": np.concatenate([core[:, 0::2], core[:, 1::2]], axis=1),
    }
    same = all(np.array_equal(np.sort(part, axis=1), np.sort(core, axis=1))
               for part in partitions.values())
    c.check("both split rules are partitions of the identical retained core",
            same, "so R_space_sampled is one number, not two")
    c.check("and that number is 1.5 on this fixture", abs(r_space - 1.5) < 1e-12,
            "R_space = %.12f" % r_space)

    # Case A: R_space inside M, so the split rule decides the disposition.
    a_cont = disposition(6.0, 5.0, r_space, cont, 10.0, 2.0)
    a_inter = disposition(6.0, 5.0, r_space, inter, 10.0, 2.0)
    c.check("inside M the fixture passes on contiguous halves",
            a_cont == "passes", a_cont)
    c.check("inside M the same fixture is withheld on interleaved halves",
            a_inter == "unmeasurable", a_inter)

    # Case B: the same channels with a spatial spread outside M. The split's
    # R_null values are unchanged, because base cancels out of r_c.
    loud = parity_core(ratios, [1.0] * 64 + [3.0] * 8)
    b_space = spread(sigma_hat(loud))
    b_cont = spread(sigma_hat(loud[:, :HALF]) / sigma_hat(loud[:, HALF:]))
    b_inter = spread(sigma_hat(loud[:, 0::2]) / sigma_hat(loud[:, 1::2]))
    c.check("scaling eight channels leaves both R_null values where they were",
            abs(b_cont - cont) < 1e-12 and abs(b_inter - inter) < 1e-12,
            "%.12f / %.12f" % (b_cont, b_inter))
    c.check("but it carries R_space_sampled outside strict M",
            b_space > 2.0, "R_space = %.12f" % b_space)
    d_cont = disposition(6.0, 5.0, b_space, b_cont, 10.0, 2.0)
    d_inter = disposition(6.0, 5.0, b_space, b_inter, 10.0, 2.0)
    c.check("outside M the split rule cannot change the disposition",
            d_cont == d_inter == "fails-homogeneity-resolved",
            "%s / %s" % (d_cont, d_inter))
    records["parity"] = {"r_space": float(r_space), "contiguous": float(cont),
                         "interleaved": float(inter),
                         "loud_r_space": float(b_space),
                         "inside_M": [a_cont, a_inter],
                         "outside_M": [d_cont, d_inter]}


def timing(c, records, root):
    """T7-R2: the candidate declares no rate, so the phrase names nothing."""
    c.heading("5. T7-R2  what 'the candidate's own declared rate' would name")
    path = os.path.join(root, TIMING_REL)
    entry = None
    for line in io.open(path, encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        row = json.loads(line)
        if row.get("session") == RANK1_SESSION:
            entry = row
            break
    c.check("rank 1's entry is in the timing index", entry is not None)
    if entry is None:
        return
    series = [s for s in entry["series"] if s["name"] == RANK1_SERIES]
    c.check("rank 1's raw AP series is present", len(series) == 1)
    s = series[0]
    c.check("its timing source is timestamps, not a declared rate",
            s["timing_source"] == "timestamps", s["timing_source"])
    c.check("so `rate_hz` is this project's whole-span derivation",
            abs(s["rate_hz"] - 30000.039869961383) < 1e-9,
            "%.12f Hz" % s["rate_hz"])
    head = s["head"]["rate_from_mean_hz"]
    c.check("the first 1,000 timestamps give a different figure",
            abs(head - s["rate_hz"]) > 1e-9, "%.12f Hz" % head)
    records["timing"] = {"timing_source": s["timing_source"],
                         "rate_hz": s["rate_hz"], "head_rate_hz": head}


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[0],
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", required=True,
                        help="project root, used only for the timing index")
    parser.add_argument("--out", required=True,
                        help="path for the human-readable check report")
    parser.add_argument("--records", default=None,
                        help="optional path for the JSON record")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    root = os.path.abspath(args.repo_root)
    c = Checks()
    records = {}
    ground_one(c, records)
    ground_three(c, records)
    reach(c, records)
    parity(c, records)
    timing(c, records, root)

    text = c.render()
    sys.stdout.write(text)
    io.open(args.out, "w", encoding="utf-8", newline="\n").write(text)
    if args.records:
        io.open(args.records, "w", encoding="utf-8", newline="\n").write(
            json.dumps(records, indent=2, sort_keys=True) + "\n")
    return 1 if c.failed else 0


if __name__ == "__main__":
    sys.exit(main())
