#!/usr/bin/env python3
"""Exact colored-Levi comparison of CFG23 E1, E2, and Cuntz CT-1.

BLISS (through python-igraph) supplies canonical labels. NetworkX VF2 is an
independent exact isomorphism oracle and directly checks the returned edge map.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import igraph as ig
import networkx as nx

ROOT = Path(__file__).resolve().parents[2]


def load_tables():
    e1 = json.loads((ROOT / "coordinates.json").read_text(encoding="utf-8"))
    e2 = json.loads((ROOT / "evidence" / "e2" / "witness.json").read_text(encoding="utf-8"))
    ct = json.loads((ROOT / "evidence" / "ct1" /
                     "ct1_reconstruction.json").read_text(encoding="utf-8"))
    return {
        "E1-rational": e1["line_incident_points"],
        "E2-quadratic": e2["line_incident_points"],
        "CT1-S1": ct["ct1_incidence"]["line_incidences_by_point_id"],
    }


def validate(name, rows):
    assert len(rows) == 23 and all(len(set(r)) == 4 for r in rows), name
    assert all(0 <= p < 23 for r in rows for p in r), name
    degrees = [sum(p in r for r in rows) for p in range(23)]
    assert degrees == [4] * 23, (name, degrees)
    assert len({tuple(sorted(r)) for r in rows}) == 23, name


def nx_graph(rows, swap=False):
    g = nx.Graph()
    for p in range(23):
        g.add_node(("P", p), role="L" if swap else "P")
    for l in range(23):
        g.add_node(("L", l), role="P" if swap else "L")
    for l, ps in enumerate(rows):
        for p in ps:
            g.add_edge(("P", p), ("L", l))
    return g


def vf2(a, b, swap_b=False):
    ga, gb = nx_graph(a), nx_graph(b, swap=swap_b)
    gm = nx.algorithms.isomorphism.GraphMatcher(
        ga, gb, node_match=lambda x, y: x["role"] == y["role"]
    )
    if not gm.is_isomorphic():
        return False
    m = gm.mapping
    mapped = {frozenset((m[u], m[v])) for u, v in ga.edges}
    assert mapped == {frozenset(e) for e in gb.edges}
    return True


def permutation_order(mapping):
    seen = set()
    order = 1
    for x in mapping:
        if x in seen:
            continue
        y, n = x, 0
        while y not in seen:
            seen.add(y)
            y = mapping[y]
            n += 1
        order = math.lcm(order, n)
    return order


def automorphism_profile(rows):
    g = nx_graph(rows)
    gm = nx.algorithms.isomorphism.GraphMatcher(
        g, g, node_match=lambda x, y: x["role"] == y["role"]
    )
    autos = [dict(m) for m in gm.isomorphisms_iter()]
    hist = {}
    for m in autos:
        n = permutation_order(m)
        hist[str(n)] = hist.get(str(n), 0) + 1
    abelian = all(
        all(a[b[x]] == b[a[x]] for x in g.nodes)
        for a in autos for b in autos
    )
    return len(autos), hist, abelian


def uncolored_levi_automorphism_count(rows):
    g = nx_graph(rows)
    return sum(1 for _ in nx.algorithms.isomorphism.GraphMatcher(g, g).isomorphisms_iter())


def bliss_digest(rows):
    # Vertices 0..22 are points; 23..45 are lines. Distinct colors force the
    # part-preserving notion used throughout the campaign.
    edges = [(p, 23 + l) for l, ps in enumerate(rows) for p in ps]
    g = ig.Graph(n=46, edges=edges, directed=False)
    colors = [0] * 23 + [1] * 23
    perm = g.canonical_permutation(color=colors)
    cg = g.permute_vertices(perm)
    bits = bytearray(46 * 46)
    for u, v in cg.get_edgelist():
        bits[u * 46 + v] = bits[v * 46 + u] = 1
    return hashlib.sha256(bits).hexdigest()


def relabel(rows):
    # Two invertible affine permutations mod 23, applied independently.
    pp = {i: (7 * i + 3) % 23 for i in range(23)}
    lp = {i: (11 * i + 5) % 23 for i in range(23)}
    out = [[] for _ in range(23)]
    for l, ps in enumerate(rows):
        out[lp[l]] = [pp[p] for p in ps]
    return out


def main():
    tables = load_tables()
    for name, rows in tables.items():
        validate(name, rows)
    objects = {}
    for name, rows in tables.items():
        aut_order, aut_hist, aut_abelian = automorphism_profile(rows)
        objects[name] = {
            "bliss_colored_levi_sha256": bliss_digest(rows),
            "part_preserving_automorphism_order_vf2": aut_order,
            "part_preserving_element_order_histogram": aut_hist,
            "part_preserving_group_abelian": aut_abelian,
            "full_uncolored_levi_automorphism_order_vf2": uncolored_levi_automorphism_count(rows),
            "self_dual_vf2": vf2(rows, rows, swap_b=True),
            "bliss_relabel_control_pass": bliss_digest(rows) == bliss_digest(relabel(rows)),
            "vf2_relabel_control_pass": vf2(rows, relabel(rows)),
        }
    comparisons = []
    names = list(tables)
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            comparisons.append({
                "a": a,
                "b": b,
                "bliss_digest_equal": objects[a]["bliss_colored_levi_sha256"] == objects[b]["bliss_colored_levi_sha256"],
                "vf2_part_preserving_isomorphic": vf2(tables[a], tables[b]),
                "vf2_part_swapping_isomorphic": vf2(tables[a], tables[b], swap_b=True),
            })
    report = {
        "schema": "cfg23-p3-isomorphism-audit-v1",
        "python_igraph_version": ig.__version__,
        "networkx_version": nx.__version__,
        "objects": objects,
        "comparisons": comparisons,
    }
    out = Path(__file__).with_name("isomorphism_receipt.json")
    out.write_bytes((json.dumps(report, indent=2) + "\n").encode())
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
