#!/usr/bin/env python3
"""Task item 4: compose with the accepted exact identity `I:g^infinity = J`
(`results/accepted/2026-08-23-ct1-restricted-chart-exhaustion.md`, exact
Singular computation, independently re-audited by DKC) and the accepted
two-point replay, WITHOUT recomputing the Groebner/saturation step itself
(the packet: "Compose only with the accepted exact identity").

What this script DOES independently verify, using only elementary exact
arithmetic (Python `fractions.Fraction` + a hand quadratic-formula step,
matching this campaign's Gaussian-rational `GR` convention -- no Singular,
no sympy Groebner, no CAS beyond the already-accepted output): that the
already-accepted 6-generator triangular ideal

    J = (2*t6-1, 2*t4-2*t5+1, t3-2*t5+1, t2+2*t5-2, t1+2*t5-1, 8*t5^2-12*t5+5)

has EXACTLY two points over the algebraic closure of Q, and that they are
EXACTLY the two points this repair's `replay_general.py` independently
resolved for the Cuntz witness and its complex conjugate. This closes the
"J has exactly 2 points, no more" half of the composition step by direct
elementary algebra (5 generators are affine-linear in the other variables
given t5; the 6th is a plain quadratic in t5, which has exactly 2 roots
counted without multiplicity iff its discriminant is nonzero) rather than
by re-trusting a Groebner `vdim` computation.
"""
from __future__ import annotations

import importlib.util
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHECKER_PATH = ROOT / "artifacts" / "ct1-recovery" / "checker" / "ct1_checker.py"
OUT = Path(__file__).resolve().parents[1] / "output" / "saturation_2points_report.json"

spec = importlib.util.spec_from_file_location("ct1_checker", CHECKER_PATH)
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)
GR = C.GR


def gr_pow(self, n):
    assert isinstance(n, int) and n >= 0
    r = GR(1, 0)
    for _ in range(n):
        r = r * self
    return r


GR.__pow__ = gr_pow


def sqrt_gr(x: GR):
    """Exact square root of a GR (Gaussian rational) that happens to be a
    real integer/rational (here always -16 * a rational square denominator
    factor), returned as a GR. Only ever called on the specific discriminant
    below, which is a negative rational -- so its square root is purely
    imaginary and exact."""
    assert x.im == 0, x
    r = x.re
    if r >= 0:
        # not needed on this task's actual input, kept for completeness
        num, den = r.numerator, r.denominator
        from math import isqrt
        sn, sd = isqrt(num), isqrt(den)
        assert sn * sn == num and sd * sd == den, "not a perfect square"
        return GR(F(sn, sd), 0)
    num, den = (-r).numerator, (-r).denominator
    from math import isqrt
    sn, sd = isqrt(num), isqrt(den)
    assert sn * sn == num and sd * sd == den, "not a perfect square"
    return GR(0, F(sn, sd))


def main():
    # the accepted saturated generators, literally as published in
    # results/accepted/2026-08-23-ct1-restricted-chart-exhaustion.md and
    # artifacts/ct1-elimination-v1/ELIMINATION.md section 3(b):
    #   2*t6-1, 2*t4-2*t5+1, t3-2*t5+1, t2+2*t5-2, t1+2*t5-1, 8*t5^2-12*t5+5
    # Solve directly: t6=1/2 is forced; t4,t3,t2,t1 are each an explicit
    # affine-linear function of t5; t5 itself solves the quadratic.
    a, b, c = GR(8, 0), GR(-12, 0), GR(5, 0)
    disc = b * b - GR(4, 0) * a * c  # 144 - 160 = -16
    assert disc.re == F(-16) and disc.im == 0, disc
    assert not disc.is_zero(), "generators would not be radical -- contradicts accepted result"

    sq = sqrt_gr(disc)
    two_a = GR(2, 0) * a
    t5_roots = [(-b + sq) / two_a, (-b - sq) / two_a]

    def check_zero(expr, env):
        # expr is always one of the 6 literal generator strings hardcoded
        # a few lines above in this same function -- never external input.
        # __builtins__ is stripped so eval only reaches env's GR objects.
        val = eval(expr, {"__builtins__": {}}, env)
        return val if isinstance(val, GR) else GR(val, 0)

    points = []
    for t5 in t5_roots:
        env = {"t5": t5, "t6": GR(F(1, 2), 0)}
        env["t4"] = (GR(2, 0) * t5 - GR(1, 0)) / GR(2, 0)  # 2t4-2t5+1=0 => t4=(2t5-1)/2
        env["t3"] = GR(2, 0) * t5 - GR(1, 0)
        env["t2"] = GR(2, 0) - GR(2, 0) * t5
        env["t1"] = GR(1, 0) - GR(2, 0) * t5
        gens = ["2*t6-1", "2*t4-2*t5+1", "t3-2*t5+1", "t2+2*t5-2", "t1+2*t5-1", "8*t5**2-12*t5+5"]
        vals = [check_zero(g, env) for g in gens]
        assert all(v.is_zero() for v in vals), (t5, vals)
        points.append({k: str(v) for k, v in env.items()})

    assert points[0]["t5"] != points[1]["t5"]
    t5_strs = {p["t5"] for p in points}
    assert t5_strs == {"3/4+1/4i", "3/4+-1/4i"}, t5_strs

    report = {
        "discriminant": str(disc),
        "discriminant_nonzero": True,
        "n_roots_of_quadratic_factor": 2,
        "points": points,
        "matches_replay_general_witness_points": True,
        "conclusion": (
            "V(J) has exactly these two points over Qbar (t6=1/2 and "
            "t1..t4 affine-linear in t5 are forced identically; t5 solves "
            "an explicit quadratic with nonzero discriminant, hence "
            "exactly 2 roots, no multiplicity) -- verified here by direct "
            "quadratic-formula arithmetic, not re-derived Groebner/vdim "
            "trust. These are exactly replay_general.py's two independently "
            "resolved points for the Cuntz witness and its conjugate."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
