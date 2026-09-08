"""Exact (symbolic) verification of the point-orbit menus used in
DK SYMMETRY ACTION CLASSIFICATION PACKET v1.

For each finite 2-subgroup family (cyclic Z/n and dihedral D_n, n a power of
2, embedded in SO(3) <= PGL_3(R) via the canonical rotation representation)
this script:

  1. Builds every group element as an EXACT 3x3 matrix over a number field
     (rationals extended by the relevant algebraic cosines/sines -- sympy
     produces closed radical forms for cos(pi/4), cos(pi/8), etc. exactly,
     no floating point anywhere).
  2. For a battery of representative points (the pole F, a generic point of
     the invariant line L, the two "special" reflection-axis points on L for
     the dihedral case, and a fully generic point), computes the EXACT
     stabilizer (by symbolic projective-equality testing: two vectors
     represent the same point of RP^2 iff their 2x2 cross-products all
     vanish after sympy.simplify) and hence the exact orbit size.
  3. Cross-checks every computed orbit size against the closed-form menu
     claimed in the inbox report:
         cyclic Z/n            : {1, n/2, n}
         dihedral D_n (order2n): {1, n/2 (x2 families), n, 2n}

No claim in this script is treated as deciding anything about real (23_4)
realizability; it only certifies the abstract SO(3)-orbit combinatorics used
downstream by hand in the report. decides=[] for this file in isolation --
the numbers it prints are then combined, in the report, with the accepted
(23_4) axioms (exactly-4 regularity) by ordinary integer arithmetic.
"""
import json
import sys
from pathlib import Path

import sympy as sp

x, y, z = sp.symbols("x y z")


def rot_z(theta):
    c, s = sp.cos(theta), sp.sin(theta)
    return sp.Matrix([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def rot_x_180():
    return sp.diag(1, -1, -1)


def same_projective_point(u, v):
    """Exact test: u, v (length-3 sympy vectors) represent the same point
    of RP^2, i.e. are linearly dependent. Tests all three 2x2 minors of the
    stacked matrix and simplifies each to zero."""
    for i in range(3):
        j = (i + 1) % 3
        minor = sp.simplify(u[i] * v[j] - u[j] * v[i])
        if minor != 0:
            return False
    return True


def apply(M, p):
    return sp.simplify(M * sp.Matrix(p))


def orbit(group, p):
    pts = []
    for g in group:
        gp = apply(g, p)
        if not any(same_projective_point(gp, q) for q in pts):
            pts.append(gp)
    return pts


def cyclic_group(n):
    theta = sp.pi * 2 / n
    R = rot_z(theta)
    elems = [sp.eye(3)]
    cur = sp.eye(3)
    for _ in range(n - 1):
        cur = sp.simplify(cur * R)
        elems.append(cur)
    return elems


def dihedral_group(n):
    cyc = cyclic_group(n)
    S = rot_x_180()
    return cyc + [sp.simplify(S * g) for g in cyc]


def check_family(n, kind):
    """kind in {'cyclic','dihedral'}. Returns dict of test-point -> orbit size."""
    group = cyclic_group(n) if kind == "cyclic" else dihedral_group(n)
    order = len(group)
    assert order == (n if kind == "cyclic" else 2 * n)

    F = [0, 0, 1]  # pole
    generic_on_L = [2, 3, 0]  # a "random" point of L = {z=0}
    special_1_on_L = [1, 0, 0]  # center of the reflection s (dihedral only)
    special_2_on_L = [0, 1, 0]  # center of the reflection s*r^{n/2} (dihedral only)
    generic_point = [1, 2, 3]  # fully generic

    results = {}
    for name, p in [
        ("F_pole", F),
        ("generic_on_L", generic_on_L),
        ("special_on_L_1", special_1_on_L),
        ("special_on_L_2", special_2_on_L),
        ("generic_point", generic_point),
    ]:
        results[name] = len(orbit(group, p))
    return {"n": n, "kind": kind, "group_order": order, "orbit_sizes": results}


def main():
    out = []
    for n in [2, 4, 8, 16]:
        out.append(check_family(n, "cyclic"))
    for n in [2, 4, 8]:
        out.append(check_family(n, "dihedral"))

    expected = {}
    for n in [2, 4, 8, 16]:
        expected[(n, "cyclic")] = {
            "F_pole": 1,
            "generic_on_L": n // 2,
            "special_on_L_1": n // 2,
            "special_on_L_2": n // 2,
            "generic_point": n,
        }
    for n in [2, 4, 8]:
        expected[(n, "dihedral")] = {
            "F_pole": 1,
            "generic_on_L": n,
            "special_on_L_1": n // 2,
            "special_on_L_2": n // 2,
            "generic_point": 2 * n,
        }

    all_ok = True
    for rec in out:
        key = (rec["n"], rec["kind"])
        exp = expected[key]
        got = rec["orbit_sizes"]
        ok = (exp == got)
        all_ok = all_ok and ok
        rec["expected"] = exp
        rec["matches_hand_derivation"] = ok

    payload = {"all_match": all_ok, "records": out}
    Path(__file__).with_name("output").mkdir(exist_ok=True)
    outpath = Path(__file__).with_name("output") / "orbit_structure.json"
    outpath.write_text(json.dumps(payload, indent=2, default=str))
    print(json.dumps(payload, indent=2, default=str))
    if not all_ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
