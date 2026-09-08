#!/usr/bin/env python3
"""Machine checks of the FINITE parts of this lane's re-derivation
(../PROOFS.md).  These are exhaustive checks of statements that are
finite by nature; they replace no proof, they only rule out transcription
error in the case table, the frame arithmetic and the cell list.

C1  incidence-orbit case table, rows 1-10: exhaustive over all
    V4-invariant flag relations between one point orbit and one line orbit.
C2  Theorem A: exhaustive over all (f, f*, chosen vertex/axis sets, b, b*)
    integer frames satisfying the forced-degree equations of rows 1-4.
C3  Lemma D corollaries and the six-cell theorem: exhaustive over the 54
    nominal sub-cells.
C4  Real projective model check: the diag(+-1) V4 on RP^2 over the
    rationals -- fixed sets, axes, vertices, and the row 1-4/8 forcings,
    verified on exact rational sample data.
"""

import itertools
import json
import os
from collections import defaultdict

V4 = (0, 1, 2, 3)
NONTRIV = (1, 2, 3)


# ----------------------------------------------------------------------
# C1: the case table
# ----------------------------------------------------------------------

def subgroups():
    """(name, frozenset) for 1, <s_i>, V4"""
    out = [('1', frozenset({0}))]
    for i in NONTRIV:
        out.append(('<s%d>' % i, frozenset({0, i})))
    out.append(('V4', frozenset(V4)))
    return out


def cosets(H):
    """the V4/H coset space as a list of frozensets, plus the action"""
    cs = []
    for g in V4:
        c = frozenset(g ^ h for h in H)
        if c not in cs:
            cs.append(c)
    cs.sort(key=lambda c: min(c))
    idx = {c: i for i, c in enumerate(cs)}
    act = [[idx[frozenset(g ^ x for x in c)] for c in cs] for g in V4]
    return cs, act


def case_table():
    """For every (point-orbit stabiliser, line-orbit stabiliser) pair,
    enumerate ALL V4-invariant incidence relations and report:
      n_flag_orbits  : number of V4-orbits of flags ("classes")
      max_classes_ok : the largest number of simultaneous classes that
                       does NOT violate the pair condition
      per_class      : (point degree gain, line degree gain) per class
    The pair condition here is exactly `two distinct points on two distinct
    lines' RESTRICTED to the two orbits (which is what the derivation's
    [ABS] arguments use)."""
    res = {}
    for pn, H in subgroups():
        for ln, K in subgroups():
            P, pact = cosets(H)
            L, lact = cosets(K)
            npt, nln = len(P), len(L)
            # V4-orbits on P x L
            seen = set()
            orbits = []
            for i in range(npt):
                for j in range(nln):
                    if (i, j) in seen:
                        continue
                    o = frozenset((pact[g][i], lact[g][j]) for g in V4)
                    seen |= set(o)
                    orbits.append(sorted(o))
            best = 0
            per_class = set()
            for o in orbits:
                dp = defaultdict(int)
                dl = defaultdict(int)
                for (i, j) in o:
                    dp[i] += 1
                    dl[j] += 1
                per_class.add((max(dp.values()), max(dl.values())))
            for r in range(len(orbits), 0, -1):
                found = False
                for sub in itertools.combinations(range(len(orbits)), r):
                    flags = set()
                    for k in sub:
                        flags |= set(orbits[k])
                    ok = True
                    for (i1, i2) in itertools.combinations(range(npt), 2):
                        for (j1, j2) in itertools.combinations(range(nln), 2):
                            if all(f in flags for f in
                                   ((i1, j1), (i1, j2), (i2, j1), (i2, j2))):
                                ok = False
                                break
                        if not ok:
                            break
                    if ok:
                        found = True
                        break
                if found:
                    best = r
                    break
            res['%s x %s' % (pn, ln)] = {
                'orbit_sizes': (npt, nln),
                'n_flag_orbits': len(orbits),
                'max_simultaneous_classes_pair_ok': best,
                'per_class_degree_gain_point_line': sorted(per_class),
            }
    return res


# ----------------------------------------------------------------------
# C2: Theorem A, exhaustively over integer frames
# ----------------------------------------------------------------------

def theorem_A_search(n=23):
    """Enumerate every (V, W, b, b*, a, a*) with
         V, W subsets of {1,2,3}   (chosen vertices / chosen axes)
         b_i, b*_i >= 0, a, a* >= 0
       satisfying
         (i)   n = |V| + 2 sum b_i + 4a       and dually
         (ii)  for each i in V:  |W \\ {i}| + 2 b*_i = 4     [rows 1,2,3]
         (iii) for each i in W:  |V \\ {i}| + 2 b_i  = 4     [rows 1,4,8]
       and report the surviving frames."""
    sols = []
    for fV in range(4):
        for V in itertools.combinations(NONTRIV, fV):
            for fW in range(4):
                for W in itertools.combinations(NONTRIV, fW):
                    # b*_i forced for i in V, b_i forced for i in W
                    bstar = {}
                    ok = True
                    for i in V:
                        rem = 4 - len([w for w in W if w != i])
                        if rem < 0 or rem % 2:
                            ok = False
                            break
                        bstar[i] = rem // 2
                    if not ok:
                        continue
                    b = {}
                    for i in W:
                        rem = 4 - len([v for v in V if v != i])
                        if rem < 0 or rem % 2:
                            ok = False
                            break
                        b[i] = rem // 2
                    if not ok:
                        continue
                    for bfree in itertools.product(range(0, 12), repeat=3):
                        bb = list(bfree)
                        good = True
                        for i in W:
                            if bb[i - 1] != b[i]:
                                good = False
                        if not good:
                            continue
                        rest = n - len(V) - 2 * sum(bb)
                        if rest < 0 or rest % 4:
                            continue
                        a = rest // 4
                        for bsfree in itertools.product(range(0, 12), repeat=3):
                            bs = list(bsfree)
                            good = True
                            for i in V:
                                if bs[i - 1] != bstar[i]:
                                    good = False
                            if not good:
                                continue
                            rest2 = n - len(W) - 2 * sum(bs)
                            if rest2 < 0 or rest2 % 4:
                                continue
                            astar = rest2 // 4
                            sols.append({'V': list(V), 'W': list(W), 'b': bb,
                                         'a': a, 'bstar': bs, 'astar': astar})
    return sols


def theorem_A_frames(n=23):
    """The Theorem-A conclusion, checked: among all frames above, which
    (|V|,|W|) shapes survive?  We report the set of (f, f*, same-index?)."""
    sols = theorem_A_search(n)
    shapes = set()
    for s in sols:
        same = (len(s['V']) == 1 and len(s['W']) == 1 and s['V'] == s['W'])
        shapes.add((len(s['V']), len(s['W']), same))
    return sorted(shapes), len(sols)


# ----------------------------------------------------------------------
# C3: the 54 nominal sub-cells and the six-cell theorem
# ----------------------------------------------------------------------

def nominal_subcells():
    out = []
    for b in (1, 3, 5):
        for bs in (1, 3, 5):
            if 16 - 2 * b - 2 * bs < 0:
                continue
            for b2 in range(b + 1):
                for bs2 in range(bs + 1):
                    key = (b2, b - b2, bs2, bs - bs2)
                    if (key[1], key[0], key[3], key[2]) < key:
                        continue
                    out.append(key)
    return sorted(out)


def six_cell_theorem():
    """Apply the Lemma-D corollaries  2 b_i <= a*  and  2 b*_i <= a
    (i in {2,3}), plus 2 <= a, 2 <= a*, to the 54 nominal sub-cells."""
    surv, dead = [], []
    for (b2, b3, bs2, bs3) in nominal_subcells():
        b, bs = b2 + b3, bs2 + bs3
        a, astar = (18 - 2 * b) // 4, (18 - 2 * bs) // 4
        why = []
        if a < 2:
            why.append('a<2')
        if astar < 2:
            why.append('astar<2')
        if 2 * b2 > astar:
            why.append('2b2>astar')
        if 2 * b3 > astar:
            why.append('2b3>astar')
        if 2 * bs2 > a:
            why.append('2bs2>a')
        if 2 * bs3 > a:
            why.append('2bs3>a')
        name = 'n23-fence-b%d%d-bs%d%d' % (b2, b3, bs2, bs3)
        (surv if not why else dead).append((name, why))
    return surv, dead


# ----------------------------------------------------------------------
# C4: exact rational model of V4 <= PGL_3(Q) <= PGL_3(R)
# ----------------------------------------------------------------------

from fractions import Fraction


def _norm(v):
    """normalise a projective point/line vector over Q to a canonical form"""
    v = [Fraction(x) for x in v]
    for x in v:
        if x != 0:
            v = [y / x for y in v]
            break
    return tuple(v)


def real_model_checks():
    S = {1: (-1, 1, 1), 2: (1, -1, 1), 3: (1, 1, -1)}

    def act_pt(i, p):
        d = S[i]
        return _norm([d[k] * p[k] for k in range(3)])

    def act_ln(i, l):
        d = S[i]          # diagonal, so the dual action uses the same signs
        return _norm([d[k] * l[k] for k in range(3)])

    def incident(p, l):
        return sum(p[k] * l[k] for k in range(3)) == 0

    C = {1: _norm((1, 0, 0)), 2: _norm((0, 1, 0)), 3: _norm((0, 0, 1))}
    A = {1: _norm((1, 0, 0)), 2: _norm((0, 1, 0)), 3: _norm((0, 0, 1))}
    rep = {}
    # (a) c_i in A_j iff i != j
    rep['c_i_on_A_j_iff_i_neq_j'] = all(
        incident(C[i], A[j]) == (i != j) for i in NONTRIV for j in NONTRIV)
    # (b) V4 common fixed points are exactly the c_i, among a rational sample
    pool = [_norm(v) for v in itertools.product(range(-2, 3), repeat=3)
            if any(v)]
    pool = sorted(set(pool))
    common = [p for p in pool if all(act_pt(i, p) == p for i in NONTRIV)]
    rep['common_fixed_points_are_vertices'] = sorted(common) == sorted(C.values())
    # (c) Fix(s_i) = {c_i} u A_i, on the sample
    ok = True
    for i in NONTRIV:
        got = {p for p in pool if act_pt(i, p) == p}
        want = {p for p in pool if p == C[i] or incident(p, A[i])}
        ok &= (got == want)
    rep['Fix_s_i_equals_c_i_union_A_i'] = ok
    # (d) every line through c_i is s_i-fixed; s_i-fixed lines are A_i or
    #     through c_i
    ok = True
    for i in NONTRIV:
        for l in pool:
            thru = incident(C[i], l)
            fixed = (act_ln(i, l) == l)
            if thru and not fixed:
                ok = False
            if fixed and not (thru or l == A[i]):
                ok = False
    rep['fixed_lines_of_s_i'] = ok
    # (e) a point on A_i is s_i-fixed (the key one-liner of Lemma 5)
    rep['point_on_A_i_is_s_i_fixed'] = all(
        act_pt(i, p) == p for i in NONTRIV for p in pool if incident(p, A[i]))
    # (f) A_i n A_j = {c_k}
    ok = True
    for i in NONTRIV:
        for j in NONTRIV:
            if i >= j:
                continue
            k = ({1, 2, 3} - {i, j}).pop()
            both = [p for p in pool if incident(p, A[i]) and incident(p, A[j])]
            ok &= (both == [C[k]])
    rep['A_i_meet_A_j_is_c_k'] = ok
    # (g) a 2-orbit point of stabiliser <s_i> lies on A_i and not at a vertex
    ok = True
    for p in pool:
        st = {i for i in NONTRIV if act_pt(i, p) == p}
        if len(st) == 1:
            i = st.pop()
            ok &= incident(p, A[i]) and p not in C.values()
    rep['stab_s_i_points_lie_on_A_i'] = ok
    # (h) a free (trivial-stabiliser) point lies on no axis
    ok = True
    for p in pool:
        st = {i for i in NONTRIV if act_pt(i, p) == p}
        if not st:
            ok &= not any(incident(p, A[i]) for i in NONTRIV)
    rep['free_points_lie_on_no_axis'] = ok
    # (i) no involution of PGL_3 over Q in this family is fixed-point-free
    rep['no_fixed_point_free_involution_in_model'] = all(
        any(act_pt(i, p) == p for p in pool) for i in NONTRIV)
    return rep


def main():
    out = {
        'C1_case_table': case_table(),
        'C2_theoremA_surviving_shapes': None,
        'C3_six_cell_theorem': None,
        'C4_real_model': real_model_checks(),
    }
    shapes, nsol = theorem_A_frames(23)
    out['C2_theoremA_surviving_shapes'] = {
        'shapes_(f,fstar,same_index)': shapes,
        'n_integer_frames': nsol,
        'conclusion_f_eq_fstar_eq_1_same_index':
            all(s == (1, 1, True) for s in shapes),
    }
    shapes22, nsol22 = theorem_A_frames(22)
    out['C2_theoremA_n22_control'] = {
        'shapes_(f,fstar,same_index)': shapes22, 'n_integer_frames': nsol22}
    surv, dead = six_cell_theorem()
    out['C3_six_cell_theorem'] = {
        'n_nominal_subcells': len(surv) + len(dead),
        'surviving': [s[0] for s in surv],
        'n_dead': len(dead),
        'dead_reasons_sample': dead[:6],
    }
    d = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'item1_theory_checks.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=str)
    print(json.dumps(out, indent=1, default=str))


if __name__ == '__main__':
    main()
