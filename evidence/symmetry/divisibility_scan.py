"""Exact integer feasibility scan for the DK symmetry-action-classification
packet: given the orbit-size menu certified by verify_orbit_structure.py,
which finite 2-groups G <= PGL_3(R) can possibly act on the point set of a
real geometric (23_4) configuration at all (before any question of whether
such a configuration exists)?

This is pure Diophantine bookkeeping, exhaustively brute forced (no claim
here rests on hand arithmetic alone). It does not decide realizability of
any configuration -- decides=[] -- it only certifies which abstract group
orders are not immediately excluded by orbit-counting on 23 points plus the
"L is forced to be a configuration line with exactly 4 points" fact proved
in the report.

For G = Z/n (n = 2^k, k >= 1):
    point-orbit sizes available: {1 (F, at most one such orbit),
                                   n/2 (on L, any multiplicity),
                                   n   (off F and off L, any multiplicity)}
For G = D_n (order 2n, n = 2^k, k >= 1):
    point-orbit sizes available: {1 (F, at most one such orbit),
                                   n/2 (on L, any multiplicity -- two
                                        geometric families of equal size,
                                        merged here since only the total
                                        matters for this count),
                                   n   (generic points of L, or points off
                                        L lying on a single reflection axis),
                                   2n  (fully generic, off F, L, and every
                                        reflection axis)}

The report additionally proves (independently, by the point<->line
polarity self-duality of G <= O(3)) that F must be a configuration point
and L must be a configuration line whenever k >= 2, forcing the number of
configuration points on L to equal exactly 4 (the (23_4) exactly-4-per-line
axiom). This script checks both the unconstrained feasibility (f_L any
multiple of n/2) and the constrained one (f_L forced to exactly 4).
"""
import json
from itertools import count
from pathlib import Path


def feasible_unconstrained(total, f_F_options, unit_L, unit_off):
    """Is there f_F in f_F_options, and nonneg integers m, p with
    f_F + m*unit_L + p*unit_off == total?"""
    sols = []
    for f_F in f_F_options:
        rem = total - f_F
        if rem < 0:
            continue
        for m in range(0, rem // unit_L + 1 if unit_L else 1):
            rem2 = rem - m * unit_L
            if unit_off == 0:
                if rem2 == 0:
                    sols.append((f_F, m, 0))
                continue
            if rem2 % unit_off == 0:
                sols.append((f_F, m, rem2 // unit_off))
    return sols


def feasible_constrained(total, f_F_forced, f_L_forced, unit_off):
    """f_F and f_L pinned exactly (the k>=2 forced case); remaining R must
    be a nonneg multiple of unit_off."""
    R = total - f_F_forced - f_L_forced
    if R < 0 or R % unit_off != 0:
        return None
    return R // unit_off


def scan(max_k=6):
    records = []
    for k in range(1, max_k + 1):
        n = 2 ** k
        # --- cyclic Z/n ---
        unconstrained = feasible_unconstrained(23, [0, 1], n // 2, n)
        constrained = feasible_constrained(23, 1, 4, n) if k >= 2 else None
        records.append({
            "group": f"Z/{n}",
            "k": k,
            "n": n,
            "unconstrained_feasible": bool(unconstrained),
            "unconstrained_solutions_sample": unconstrained[:3],
            "F_and_L_forced": bool(k >= 2),
            "constrained_off_count_R": constrained,
            "constrained_feasible": (k < 2) or (constrained is not None),
        })
        # --- dihedral D_n, order 2n ---
        unconstrained_d = feasible_unconstrained(23, [0, 1], n // 2, n)
        # (off-both orbits for dihedral are n or 2n; both are multiples of
        #  n, so divisibility by n is the binding constraint either way)
        constrained_d = feasible_constrained(23, 1, 4, n) if k >= 2 else None
        records.append({
            "group": f"D_{n} (order {2*n})",
            "k": k,
            "n": n,
            "unconstrained_feasible": bool(unconstrained_d),
            "unconstrained_solutions_sample": unconstrained_d[:3],
            "F_and_L_forced": bool(k >= 2),
            "constrained_off_count_R": constrained_d,
            "constrained_feasible": (k < 2) or (constrained_d is not None),
        })
    return records


def main():
    records = scan()
    surviving = [r for r in records if r["constrained_feasible"]]
    payload = {
        "surviving_groups": [r["group"] for r in surviving],
        "records": records,
    }
    outdir = Path(__file__).with_name("output")
    outdir.mkdir(exist_ok=True)
    (outdir / "divisibility_scan.json").write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
