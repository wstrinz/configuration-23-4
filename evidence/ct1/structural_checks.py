#!/usr/bin/env python3
"""Task items 2 and 3: the sequential projective-normalization proof,
checked purely combinatorially (no coordinates, no CAS, no bihomogeneous
scheme). Independent of and never invoking the 31 rejected scalar CHART
guards `L(v) = v0 + 2 v1 + 5 v2 != 0`.

This reproduces the DISTINCTNESS argument the rejected capstone certificate
used (`capstone_coverage_certificate.py` item 3, "31 CHART guards are
redundant") but stops at the conclusion that argument actually supports --
"the constructed cross-product vector is nonzero" -- and never takes the
extra (false) step "...therefore the specific linear functional L(v) is
nonzero" that the coordinator rejected. No CHART guard, and no `L(v)`
expression, is read or evaluated anywhere in this file.

Lemma B (global distinctness, re-derived here independently of
`build_presentation.py`'s `structural_sanity`, from `ct1_reconstruction.json`
directly): for any two DISTINCT declared point ids p != q, and ANY
realization phi of CT1-S1 (any assignment of the 23 points/23 lines to
P^2(K) satisfying every prescribed incidence and every prescribed
non-incidence, i.e. the genuine "exactly four" (23,23,4,4) condition, not
merely the closed incidence scheme -- EVIDENCE_POLICY.md's explicit
boundary), phi(p) != phi(q) as vectors. Proof: p has exactly 4 config
lines; p and q share at most 1 config line (checked combinatorially below);
so at least 3 of p's lines are NOT among q's. Pick one such line L. L is
prescribed through p (phi(L).phi(p) = 0) and NOT prescribed through q, i.e.
(L,q) is one of the declared 437 forbidden-fifth guards, so
phi(L).phi(q) != 0 for ANY valid realization. If phi(p) = phi(q), then
phi(L).phi(q) = phi(L).phi(p) = 0, contradiction. Hence phi(p) != phi(q).
Dually for lines.

Consequence used at every `meet`/`join` step of the construction log: if a
step combines two DECLARED-DISTINCT ids p != q (points, for a `meet`
building a line; or lines, for a `join` building a point), the cross
product phi(p) x phi(q) is nonzero for every realization phi -- because a
cross product of two vectors is zero iff the vectors are proportional, and
two distinct nonzero points/lines of P^2 are never coordinate-proportional
representatives of the same projective point/line by definition of "the
same point" (each id already denotes one specific, already-realized,
already-nonzero projective point/line; the only way the cross product could
vanish is phi(p) and phi(q) representing the SAME point, which Lemma B
rules out). No scalar functional of the vector is ever needed for this
step: "nonzero cross product" is exactly and only "the two projective
objects are distinct", which Lemma B gives directly.
"""
from __future__ import annotations

import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RECON_JSON = ROOT / "artifacts" / "ct1-recovery" / "output" / "ct1_reconstruction.json"
PRESENTATION_JSON = ROOT / "artifacts" / "ct1-realization-v1" / "output" / "presentation.json"
STRATUM_JSON = ROOT / "artifacts" / "ct1-chart-cover-v1" / "output" / "stratum_sweep_report.json"
OUT = Path(__file__).resolve().parents[1] / "output" / "structural_checks_report.json"

N = 23


def load_structure():
    data = json.loads(RECON_JSON.read_text(encoding="utf-8"))
    ct1 = data["ct1_incidence"]
    line_pts = [list(x) for x in ct1["line_incidences_by_point_id"]]
    point_lines = [[] for _ in range(N)]
    for li, pts in enumerate(line_pts):
        for p in pts:
            point_lines[p].append(li)
    for p in range(N):
        assert len(point_lines[p]) == 4
        point_lines[p].sort()
    return line_pts, point_lines


def check_at_most_one_shared(line_pts, point_lines):
    for l1, l2 in itertools.combinations(range(N), 2):
        shared = set(line_pts[l1]) & set(line_pts[l2])
        assert len(shared) <= 1, (l1, l2, shared)
    for p1, p2 in itertools.combinations(range(N), 2):
        shared = set(point_lines[p1]) & set(point_lines[p2])
        assert len(shared) <= 1, (p1, p2, shared)
    return True


def forbidden_fifth_witness_for_pair_of_points(p, q, point_lines, line_pts):
    """Lemma B instance for a point pair: return a (line, point) forbidden-
    fifth pair proving phi(p) != phi(q), for ANY two distinct declared point
    ids p != q. Exists by check_at_most_one_shared (p,q share <=1 line, p
    has 4, so >=3 candidates)."""
    assert p != q
    shared = set(point_lines[p]) & set(point_lines[q])
    assert len(shared) <= 1
    candidates = [l for l in point_lines[p] if l not in point_lines[q]]
    assert candidates, (p, q, "no witness line -- Lemma B would fail")
    L = candidates[0]
    assert q not in line_pts[L]
    assert p in line_pts[L]
    return {"line": L, "point": q}


def forbidden_fifth_witness_for_pair_of_lines(l1, l2, point_lines, line_pts):
    """Dual of the above: a (line, point) pair proving phi(l1) != phi(l2)
    as line vectors, for distinct declared line ids l1 != l2."""
    assert l1 != l2
    shared = set(line_pts[l1]) & set(line_pts[l2])
    assert len(shared) <= 1
    candidates = [p for p in line_pts[l1] if p not in line_pts[l2]]
    assert candidates, (l1, l2, "no witness point -- dual Lemma B would fail")
    P = candidates[0]
    assert P not in line_pts[l2]
    assert P in line_pts[l1]
    return {"line": l2, "point": P}


def check_frame_general_position(line_pts, point_lines):
    """Re-derive COVERAGE.md section 4 independently: {0,1,4,11} cannot be
    made collinear in any triple, for any realization, purely
    combinatorially. Returns the 4 forbidden-fifth witnesses."""
    frame = [0, 1, 4, 11]
    witnesses = {}
    config_line = {}
    for a, b in itertools.combinations(frame, 2):
        shared = set(point_lines[a]) & set(point_lines[b])
        if shared:
            (l,) = shared if len(shared) == 1 else (sorted(shared)[0],)
            config_line[(a, b)] = next(iter(shared))
    for triple in itertools.combinations(frame, 3):
        pair_lines = {}
        for a, b in itertools.combinations(triple, 2):
            key = (a, b) if (a, b) in config_line else (b, a)
            if key in config_line:
                pair_lines[(a, b)] = config_line[key]
        assert len(pair_lines) >= 2, (triple, "not enough declared config lines to force a contradiction")
        items = list(pair_lines.items())
        (pair0, l0), (pair1, l1) = items[0], items[1]
        assert l0 != l1, (triple, "two different pairs already share the same config line -- unexpected")
        # if the triple were collinear, the actual geometric lines through
        # (pair0) and (pair1) would have to coincide (both equal the unique
        # line through all 3 points) -- but l0 != l1 are DISTINCT declared
        # line ids, so this is exactly a Lemma-B-for-lines instance.
        w = forbidden_fifth_witness_for_pair_of_lines(l0, l1, point_lines, line_pts)
        witnesses[str(triple)] = {"forced_equal_lines": [l0, l1], "witness_forbidden_fifth": w}
    return witnesses


def walk_construction_log(line_pts, point_lines):
    presentation = json.loads(PRESENTATION_JSON.read_text(encoding="utf-8"))
    steps = []
    for entry in presentation["construction_log"]:
        if entry.startswith("Frame fixed") or "free parameter" in entry:
            continue
        if " := meet(" in entry:
            lid = int(entry.split(" ")[1])
            m = re.search(r"meet\(point (\d+), point (\d+)\)", entry)
            a, b = int(m.group(1)), int(m.group(2))
            w = forbidden_fifth_witness_for_pair_of_points(a, b, point_lines, line_pts)
            steps.append({"kind": "meet", "builds": f"line {lid}", "from": [a, b], "nonzero_witness": w})
        elif " := join(" in entry:
            pid = int(entry.split(" ")[1])
            m = re.search(r"join\(line (\d+), line (\d+)\)", entry)
            a, b = int(m.group(1)), int(m.group(2))
            w = forbidden_fifth_witness_for_pair_of_lines(a, b, point_lines, line_pts)
            steps.append({"kind": "join", "builds": f"point {pid}", "from": [a, b], "nonzero_witness": w})
    return steps


def check_g_factors():
    presentation = json.loads(PRESENTATION_JSON.read_text(encoding="utf-8"))
    fg = presentation["forbidden_fifth_guards"]
    by_pair = {(g["line"], g["point"]): g["expr"] for g in fg}
    targets = [
        ((1, 8), "1 - t3"),
        ((2, 11), "1 - t6"),
        ((0, 8), "t6"),
        ((1, 3), "-t2*t3 + 1"),
        ((2, 6), "-t4 + t6"),
    ]
    checks = []
    for pair, expected_expr in targets:
        actual = by_pair.get(pair)
        checks.append({"pair": pair, "expected_expr": expected_expr, "actual_expr": actual, "match": actual == expected_expr})
    assert all(c["match"] for c in checks), checks
    # confirm none of these 5 pairs is also somehow a prescribed incidence
    # (sanity: forbidden-fifth guards by construction only exist for
    # non-prescribed pairs, but re-check directly against line_pts anyway)
    line_pts, _ = load_structure()
    for pair, _ in targets:
        lid, pid = pair
        assert pid not in line_pts[lid], (pair, "should be a forbidden pair, found prescribed instead")
    return checks


def check_no_chart_guard_used():
    """Defensive check: this module's executable code never indexes
    presentation["chart_guards"] (the rejected 31-guard vocabulary) at all
    -- enforced at run time by grepping this file's own source, not merely
    by code review."""
    src = Path(__file__).read_text(encoding="utf-8")
    src_excluding_this_check, _, _ = src.partition("def check_no_chart_guard_used")
    for bad in ('["chart_guards"]', "['chart_guards']"):
        assert bad not in src_excluding_this_check, "this checker must never read the rejected CHART-guard vocabulary"
    return True


def main():
    line_pts, point_lines = load_structure()
    assert check_at_most_one_shared(line_pts, point_lines)

    frame_general_position = check_frame_general_position(line_pts, point_lines)

    steps = walk_construction_log(line_pts, point_lines)
    n_meet = sum(1 for s in steps if s["kind"] == "meet")
    n_join = sum(1 for s in steps if s["kind"] == "join")
    assert n_meet == 23, n_meet   # all 23 lines built by meet
    assert n_join == 13, n_join   # 13 of 19 non-frame points built by join

    g_factor_checks = check_g_factors()

    stratum = json.loads(STRATUM_JSON.read_text(encoding="utf-8"))
    assert stratum["n_strata"] == 63
    assert stratum["n_impossible_by_guard"] + stratum["n_impossible_by_degenerate"] == 63
    assert stratum["n_open"] == 0
    assert stratum["open_strata"] == []

    check_no_chart_guard_used()

    report = {
        "lemma_B_at_most_one_shared_line_or_point": True,
        "frame_general_position_witnesses": frame_general_position,
        "n_meet_steps_all_nonzero_by_lemma_B": n_meet,
        "n_join_steps_all_nonzero_by_lemma_B": n_join,
        "meet_join_steps": steps,
        "g_factor_forbidden_fifth_match": g_factor_checks,
        "composed_stratum_sweep_summary": {
            "n_strata": stratum["n_strata"],
            "n_impossible_by_guard": stratum["n_impossible_by_guard"],
            "n_impossible_by_degenerate": stratum["n_impossible_by_degenerate"],
            "n_open": stratum["n_open"],
            "source": "artifacts/ct1-chart-cover-v1/output/stratum_sweep_report.json (accepted, composed with, not re-derived)",
        },
        "no_CHART_guard_field_read": True,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items() if k != "meet_join_steps"}, indent=2))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
