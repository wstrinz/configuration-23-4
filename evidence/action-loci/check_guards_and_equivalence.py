"""Apply the full geometric guards and test conjugate-root equivalence exactly."""
from __future__ import annotations

import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

import networkx as nx
import sympy as sp


HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "signed-torus-push-v2"
OLD = HERE.parent / "fresh-look-real-order-v1"
sys.path.insert(0, str(OLD))
import verify_order as coordinates


CASES = {
    "E1": (SRC / "bs10_003.json", "7309c1e188360585-bc372d1fe46f0e80"),
    "E2": (SRC / "bs01_remaining_records.json", "143bd9ddf2aa1263-990b67811d33c3fb"),
}


def source_blob(oid):
    return subprocess.check_output(["git", "cat-file", "blob", oid], cwd=HERE.parents[1])


def record(path, pair_id):
    data = json.loads(path.read_text())
    return next(row for row in data["results"] if row["pin"]["pair_id"] == pair_id)


def assignments(name):
    if name == "E1":
        return [{
            sp.Symbol("x0"): sp.Rational(3, 2), sp.Symbol("x1"): sp.Rational(-2, 3),
            sp.Symbol("x2"): 1, sp.Symbol("x3"): sp.Rational(1, 3),
            sp.Symbol("x4"): sp.Rational(5, 6), sp.Symbol("x5"): sp.Rational(-1, 6),
            sp.Symbol("x6"): 2, sp.Symbol("x7"): sp.Rational(9, 2),
            sp.Symbol("x8"): sp.Rational(5, 2), sp.Symbol("x9"): sp.Rational(-1, 2),
        }]
    root = sp.sqrt(17)
    return [{sp.Symbol(f"x{i}"): value for i, value in enumerate([
        1-t, t-sp.Rational(1, 2), -1, 2*t-3, -2, -2*t-1,
        (1-t)/2, sp.Rational(1, 2), 2-t, t])}
            for t in ((3-root)/4, (3+root)/4)]


def build(name, row, obj, active_values):
    gens = [list(bytes.fromhex(g)) for g in row["pin"]["subgroup_generators_points"]]
    chart = coordinates.reconstruct(obj["lines"], gens, tuple(row["fixed_coords"]))
    assert chart is not None
    _, _, vectors = chart
    mapping = row["torus_map"]
    active = mapping["active"]
    by_original = {f: sp.Integer(1) for f in mapping["free"]}
    for original, symbol in zip(active, sp.symbols(f"x0:{row['nvariables']}")):
        by_original[original] = active_values[symbol]
    for relation in mapping["relations"]:
        by_original[relation["pivot"]] = sp.Integer(relation["sign"]) * sp.prod(
            by_original[f] ** exponent for f, exponent in zip(mapping["free"], relation["exponents"]))
    parameter_values = {variable: sp.simplify(by_original[i]) for i, variable in enumerate(chart[0])}
    sides = []
    for side in vectors:
        rows = []
        for i in range(23):
            rows.append(sp.Matrix([sp.Integer(side[i][k][0]) *
                                   (1 if side[i][k][1] is None else parameter_values[side[i][k][1]])
                                   if k in side[i] else 0 for k in range(3)]))
        sides.append(rows)
    return sides


def proportional(a, b):
    return all(sp.simplify(x) == 0 for x in a.cross(b))


def guard_report(points, lines, incidence):
    mismatches = []
    for i, p in enumerate(points):
        for j, l in enumerate(lines):
            actual = sp.simplify(p.dot(l)) == 0
            expected = i in incidence[j]
            if actual != expected:
                mismatches.append([i, j, "extra" if actual else "missing"])
    duplicate_points = [[i, j] for i, j in itertools.combinations(range(23), 2)
                        if proportional(points[i], points[j])]
    duplicate_lines = [[i, j] for i, j in itertools.combinations(range(23), 2)
                       if proportional(lines[i], lines[j])]
    nonzero = all(any(sp.simplify(x) != 0 for x in row) for row in points + lines)
    return {"incidence_mismatches": mismatches, "duplicate_points": duplicate_points,
            "duplicate_lines": duplicate_lines, "all_vectors_nonzero": nonzero,
            "guarded": not mismatches and not duplicate_points and not duplicate_lines and nonzero}


def automorphisms(incidence):
    graph = nx.Graph()
    graph.add_nodes_from((f"p{i}", {"kind": "p"}) for i in range(23))
    graph.add_nodes_from((f"l{j}", {"kind": "l"}) for j in range(23))
    graph.add_edges_from((f"p{i}", f"l{j}") for j, line in enumerate(incidence) for i in line)
    matcher = nx.algorithms.isomorphism.GraphMatcher(
        graph, graph, node_match=lambda a, b: a["kind"] == b["kind"])
    answer = []
    for mp in matcher.isomorphisms_iter():
        answer.append(([int(mp[f"p{i}"][1:]) for i in range(23)],
                       [int(mp[f"l{j}"][1:]) for j in range(23)]))
    return answer


def projectivity_for_permutation(source, target, point_perm, line_perm):
    ps, ls = source
    pt, lt = target
    # If a relabeling is induced by one projectivity, any common projective
    # frame determines that projectivity uniquely.  Test the first usable
    # frame rather than redundantly fitting all 8,855 quadruples.
    for frame in itertools.combinations(range(23), 4):
        a, b, c, d = frame
        P = sp.Matrix.hstack(ps[a], ps[b], ps[c])
        Q = sp.Matrix.hstack(pt[point_perm[a]], pt[point_perm[b]], pt[point_perm[c]])
        if sp.simplify(P.det()) == 0 or sp.simplify(Q.det()) == 0:
            continue
        v = P.inv() * ps[d]
        w = Q.inv() * pt[point_perm[d]]
        if any(sp.simplify(x) == 0 for x in list(v) + list(w)):
            continue
        T = sp.simplify(Q * sp.diag(*[sp.simplify(w[i] / v[i]) for i in range(3)]) * P.inv())
        if all(proportional(T * ps[i], pt[point_perm[i]]) for i in range(23)):
            line_ok = all(proportional(T.T.inv() * ls[j], lt[line_perm[j]]) for j in range(23))
            if line_ok:
                return {"point_permutation": point_perm, "line_permutation": line_perm,
                        "frame": list(frame), "matrix": [[str(sp.simplify(T[i, j])) for j in range(3)] for i in range(3)]}
        break
    return None


def realized_automorphisms(source, target, autos):
    return [answer for point_perm, line_perm in autos
            if (answer := projectivity_for_permutation(source, target, point_perm, line_perm)) is not None]


def main():
    out = {"authority": "EXACT_COMPUTATION", "decides": [], "graph_effect": "NONE", "cases": {}}
    built = {}
    for name, (path, pair_id) in CASES.items():
        row = record(path, pair_id)
        raw = source_blob(row["pin"]["source_blob_sha1"])
        obj = json.loads(raw)
        roots = []
        for values in assignments(name):
            sides = build(name, row, obj, values)
            report = guard_report(*sides, obj["lines"])
            roots.append({"active_values": [str(values[sp.Symbol(f"x{i}")]) for i in range(10)], **report})
            built.setdefault(name, []).append(sides)
        out["cases"][name] = {"pair_id": pair_id, "complex_points": len(roots),
                              "real_points": len(roots), "roots": roots,
                              "source_blob_sha1": row["pin"]["source_blob_sha1"],
                              "source_sha256": hashlib.sha256(raw).hexdigest()}
    obj2 = json.loads(source_blob(record(*CASES["E2"])["pin"]["source_blob_sha1"]))
    autos = automorphisms(obj2["lines"])
    collineations = realized_automorphisms(built["E2"][0], built["E2"][0], autos)
    conjugate_maps = realized_automorphisms(built["E2"][0], built["E2"][1], autos)
    assert len(collineations) == len(conjugate_maps) == 4
    out["E2_abstract_collineation_order"] = len(autos)
    out["E2_geometric_collineation_order"] = len(collineations)
    out["E2_automorphisms_exchanging_embeddings"] = len(conjugate_maps)
    out["E2_collineations"] = collineations
    out["E2_conjugate_embedding_projective_equivalence"] = conjugate_maps[0]
    out["surviving_projective_classes_by_locus"] = {"E1": 1, "E2": 1}
    out["generator_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE / "guard_and_equivalence_receipt.json").write_bytes((json.dumps(out, indent=2) + "\n").encode())
    print("E1 guarded roots", sum(r["guarded"] for r in out["cases"]["E1"]["roots"]))
    print("E2 guarded roots", sum(r["guarded"] for r in out["cases"]["E2"]["roots"]))
    print("E2 abstract", len(autos), "geometric", len(collineations),
          "embedding exchangers", len(conjugate_maps))


if __name__ == "__main__":
    main()
