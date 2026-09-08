"""Rebuild and saturate the two positive diagonal-V4 action-locus ideals.

The source equations are the immutable, encoded Q-polynomials retained by the
signed-torus sweep.  Saturation by the product of the ten torus coordinates
removes precisely the coordinate-hyperplane boundary excluded by that chart.
The script exports identical systems for SymPy, Singular, and msolve.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "signed-torus-push-v2"
CASES = {
    "E1": (SRC / "bs10_003.json", "7309c1e188360585-bc372d1fe46f0e80"),
    "E2": (SRC / "bs01_remaining_records.json", "143bd9ddf2aa1263-990b67811d33c3fb"),
}


def write_text_lf(path, value):
    path.write_bytes(value.encode())


def decode(encoded, variables):
    return sp.expand(sum(sp.Rational(c) * sp.prod(x**e for x, e in zip(variables, exponents))
                         for exponents, c in encoded))


def record(path, pair_id):
    data = json.loads(path.read_text())
    return next(row for row in data["results"] if row["pin"]["pair_id"] == pair_id)


def singular_text(name, variables, equations):
    names = ",".join(["u", *map(str, variables)])
    polys = [str(p).replace("**", "^") for p in equations]
    saturation = "u*" + "*".join(map(str, variables)) + "-1"
    xnames = ",".join(map(str, variables))
    return f'''LIB "primdec.lib";
ring r=0,({names}),lp;
ideal K={','.join(polys + [saturation])};
ideal G=std(K);
ideal J=eliminate(G,u);
ring s=0,({xnames}),lp;
ideal J=imap(r,J);
print("CASE {name}");
print("SATURATED_DIM"); print(dim(std(J)));
print("SATURATED_VDIM"); print(vdim(std(J)));
print("SATURATED_GB"); print(std(J));
list P=primdecGTZ(J);
print("PRIMARY_COMPONENT_COUNT"); print(size(P));
for (int i=1; i<=size(P); i++) {{ print("COMPONENT"); print(i); print(dim(std(P[i][1]))); print(P[i][1]); }}
'''


def msolve_text(variables, equations):
    # msolve accepts rational coefficients and computes an exact RUR with real
    # isolating intervals for a zero-dimensional ideal.
    rendered = [str(p).replace("**", "^") for p in equations]
    return ",".join(map(str, variables)) + "\n0\n" + ",\n".join(rendered) + "\n"


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    receipt = {"authority": "EXACT_COMPUTATION", "decides": [], "graph_effect": "NONE", "cases": {}}
    for name, (path, pair_id) in CASES.items():
        row = record(path, pair_id)
        variables = sp.symbols(f"x0:{row['nvariables']}")
        equations = [decode(p, variables) for p in row["initial_polynomials"]]
        u = sp.Symbol("u")
        saturation = u * sp.prod(variables) - 1
        # Lexicographic elimination of u independently reconstructs the open
        # torus ideal from the original equations, without replaying the saved
        # substitution trace.
        gb = sp.groebner([*equations, saturation], u, *variables, order="lex", domain=sp.QQ)
        eliminated = [sp.Poly(p, *variables, domain=sp.QQ).monic().as_expr()
                      for p in gb.polys if u not in p.free_symbols]
        assert eliminated
        write_text_lf(HERE / f"{name.lower()}_singular.sing", singular_text(name, variables, equations))
        write_text_lf(HERE / f"{name.lower()}_msolve.in", msolve_text(variables, eliminated))
        case = {
            "pair_id": pair_id,
            "source_record": str(path.relative_to(HERE.parents[1])).replace("\\", "/"),
            "source_record_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "variables": list(map(str, variables)),
            "initial_equation_count": len(equations),
            "saturation_guard": "*".join(map(str, variables)) + " != 0",
            "sympy_saturated_lex_basis": list(map(str, eliminated)),
            "sympy_zero_dimensional": bool(sp.groebner(eliminated, *variables, order="lex", domain=sp.QQ).is_zero_dimensional),
            "sympy_version": sp.__version__,
        }
        receipt["cases"][name] = case
        print(name, "basis", len(eliminated), "zero_dim", case["sympy_zero_dimensional"], flush=True)
    receipt["generator_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    write_text_lf(HERE / "system_receipt.json", json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
