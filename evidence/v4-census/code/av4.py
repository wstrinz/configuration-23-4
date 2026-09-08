#!/usr/bin/env python3
"""av4 -- INDEPENDENT audit library for the V4 (23_4) enumeration-completeness
audit (task `v4-enumeration-completeness-audit-v1`, lane DKW-LOI).

Written from scratch against this lane's own re-derivation (see
`../PROOFS.md`).  It deliberately does NOT import, subclass, or copy the
sidecar's `v4census.py`, nor the accepted `fresh_bare_canon.py`, nor
`coherent_ir.py`.  The only shared objects are the *pinned JSON pins*,
which are read as inert data.

Conventions (deliberately different from the sidecar's labelling, so that
any agreement is agreement of mathematical content and not of labels):

  * V4 = {0,1,2,3} under XOR; the involutions are s1=1, s2=2, s3=3.
  * A "structure" is a pair (lines, perms):
      lines : tuple of n frozensets of point labels 0..n-1, |line| = 4
      perms : 4-tuple of point permutations (tuples of length n),
              perms[g] realising the action of g in V4.
    Everything below recomputes taxonomy from (lines, perms); nothing is
    read out of a producer's metadata.
"""

import hashlib
import itertools
from collections import defaultdict

V4 = (0, 1, 2, 3)
NONTRIV = (1, 2, 3)


# ----------------------------------------------------------------------
# 0.  group / action validation
# ----------------------------------------------------------------------

def compose(p, q):
    """(p . q)(x) = p(q(x))"""
    return tuple(p[q[x]] for x in range(len(q)))


def check_v4_point_representation(n, perms):
    """perms must be a faithful V4 representation on {0..n-1} with the XOR
    composition law.  Returns list of violations."""
    bad = []
    if len(perms) != 4:
        return ['rep:len!=4']
    idp = tuple(range(n))
    for g in V4:
        if len(perms[g]) != n or sorted(perms[g]) != list(range(n)):
            bad.append('rep:not_a_permutation:g=%d' % g)
    if bad:
        return bad
    if tuple(perms[0]) != idp:
        bad.append('rep:perms[0]!=id')
    for g in V4:
        for h in V4:
            if compose(perms[g], perms[h]) != tuple(perms[g ^ h]):
                bad.append('rep:xor_law_fails:g=%d,h=%d' % (g, h))
    for g in NONTRIV:
        if tuple(perms[g]) == idp:
            bad.append('rep:not_faithful_on_points:g=%d' % g)
    return bad


def induced_line_perm(lines, perms, g):
    """Induced permutation of line indices, or None if g does not preserve
    the line set."""
    idx = {l: i for i, l in enumerate(lines)}
    if len(idx) != len(lines):
        return None
    P = perms[g]
    out = []
    for l in lines:
        img = frozenset(P[p] for p in l)
        if img not in idx:
            return None
        out.append(idx[img])
    return tuple(out)


# ----------------------------------------------------------------------
# 1.  bare (n_4) axioms
# ----------------------------------------------------------------------

def validate_n4(n, lines):
    """Independent check of the bare (n_4) / linear-space-pair axioms."""
    bad = []
    if len(lines) != n:
        bad.append('n4:line_count=%d' % len(lines))
    if len(set(lines)) != len(lines):
        bad.append('n4:repeated_line')
    deg = [0] * n
    for l in lines:
        if len(l) != 4:
            bad.append('n4:line_size=%d' % len(l))
            continue
        for p in l:
            if not (0 <= p < n):
                bad.append('n4:point_out_of_range:%r' % (p,))
                continue
            deg[p] += 1
    if any(d != 4 for d in deg):
        bad.append('n4:point_degrees=%s' % sorted(set(deg)))
    seen = {}
    for i, l in enumerate(lines):
        for u, v in itertools.combinations(sorted(l), 2):
            if (u, v) in seen:
                bad.append('n4:pair_on_two_lines:%d,%d' % (u, v))
            seen[(u, v)] = i
    return bad


def validate_equivariance(n, lines, perms):
    bad = check_v4_point_representation(n, perms)
    if bad:
        return bad
    for g in NONTRIV:
        if induced_line_perm(lines, perms, g) is None:
            bad.append('equi:g=%d_does_not_preserve_line_set' % g)
    return bad


# ----------------------------------------------------------------------
# 2.  orbit taxonomy and inventory
# ----------------------------------------------------------------------

def taxonomy(n, lines, perms):
    """Returns (pstab, lstab, lperm) with stabilisers as frozensets of V4."""
    lperm = {}
    for g in V4:
        lp = induced_line_perm(lines, perms, g)
        if lp is None:
            raise ValueError('not equivariant at g=%d' % g)
        lperm[g] = lp
    pstab = [frozenset(g for g in V4 if perms[g][p] == p) for p in range(n)]
    lstab = [frozenset(g for g in V4 if lperm[g][i] == i) for i in range(len(lines))]
    return pstab, lstab, lperm


FULL = frozenset(V4)


def inventory(n, lines, perms):
    """(f, [b1,b2,b3], a, fstar, [bs1,bs2,bs3], astar) recomputed from
    the action.  Raises if some stabiliser is not 1, <s_i>, or V4."""
    pstab, lstab, _ = taxonomy(n, lines, perms)
    f = b = [0, 0, 0]
    f = sum(1 for s in pstab if s == FULL)
    b = [sum(1 for s in pstab if s == frozenset({0, i})) // 2 for i in NONTRIV]
    a = sum(1 for s in pstab if s == frozenset({0})) // 4
    fs = sum(1 for s in lstab if s == FULL)
    bs = [sum(1 for s in lstab if s == frozenset({0, i})) // 2 for i in NONTRIV]
    asx = sum(1 for s in lstab if s == frozenset({0})) // 4
    for s in pstab + lstab:
        if s not in (FULL, frozenset({0}), frozenset({0, 1}),
                     frozenset({0, 2}), frozenset({0, 3})):
            raise ValueError('impossible stabiliser %s' % sorted(s))
    # integrality of the orbit counts
    n2p = [sum(1 for s in pstab if s == frozenset({0, i})) for i in NONTRIV]
    n2l = [sum(1 for s in lstab if s == frozenset({0, i})) for i in NONTRIV]
    n4p = sum(1 for s in pstab if s == frozenset({0}))
    n4l = sum(1 for s in lstab if s == frozenset({0}))
    if any(x % 2 for x in n2p + n2l) or n4p % 4 or n4l % 4:
        raise ValueError('orbit sizes inconsistent with stabilisers')
    return f, b, a, fs, bs, asx


def orbit_partition(n, perms):
    """List of point orbits (sorted tuples)."""
    seen = set()
    out = []
    for p in range(n):
        if p in seen:
            continue
        o = tuple(sorted({perms[g][p] for g in V4}))
        for q in o:
            seen.add(q)
        out.append(o)
    return out


# ----------------------------------------------------------------------
# 3.  necessary conditions ("fences") -- independent re-derivation
# ----------------------------------------------------------------------
#
# Tags: [ABS] follows from the linear-space pair condition + equivariance
# alone; [GEO] uses the real projective plane geometry of a faithful
# V4 <= PGL_3(R) action (Lemmas 1-5 of ../PROOFS.md).  Every condition
# below is NECESSARY for an abstract type to be the type of a geometric
# V4-symmetric configuration; none is claimed sufficient.

def necessary_conditions(n, lines, perms, require_frame=True):
    """Return list of violated necessary conditions."""
    bad = []
    pstab, lstab, _ = taxonomy(n, lines, perms)
    lsets = list(lines)
    Vpts = [p for p in range(n) if pstab[p] == FULL]
    Vlns = [k for k in range(len(lsets)) if lstab[k] == FULL]
    Pi = {i: [p for p in range(n) if pstab[p] == frozenset({0, i})] for i in NONTRIV}
    Li = {i: [k for k in range(len(lsets)) if lstab[k] == frozenset({0, i})] for i in NONTRIV}
    Fp = [p for p in range(n) if pstab[p] == frozenset({0})]
    Fl = [k for k in range(len(lsets)) if lstab[k] == frozenset({0})]

    # ---- [ABS] N5: a stab-i point never lies on a stab-j line, i != j
    for i in NONTRIV:
        for j in NONTRIV:
            if i == j:
                continue
            for k in Li[j]:
                for p in Pi[i]:
                    if p in lsets[k]:
                        bad.append('ABS_N5:i=%d,j=%d,line=%d,pt=%d' % (i, j, k, p))

    # ---- [GEO] free points lie on no V4-fixed line (axis)
    for k in Vlns:
        for p in lsets[k]:
            if pstab[p] == frozenset({0}):
                bad.append('GEO_freept_on_axis:line=%d,pt=%d' % (k, p))

    # ---- [GEO] a vertex lies on no free line
    for k in Fl:
        for p in lsets[k]:
            if pstab[p] == FULL:
                bad.append('GEO_vertex_on_freeline:line=%d,pt=%d' % (k, p))

    # ---- [GEO] GF1: a stab-i line carries at most one stab-i point
    for i in NONTRIV:
        for k in Li[i]:
            c = [p for p in Pi[i] if p in lsets[k]]
            if len(c) > 1:
                bad.append('GEO_GF1:i=%d,line=%d,pts=%s' % (i, k, c))

    # ---- [GEO] GF2: a stab-i point lies on at most one stab-i LINE ORBIT
    #      (equivalently, since the two lines of one orbit meet only at c_i,
    #       on at most one stab-i line -- both forms are checked)
    for i in NONTRIV:
        for p in Pi[i]:
            c = [k for k in Li[i] if p in lsets[k]]
            if len(c) > 1:
                bad.append('GEO_GF2:i=%d,pt=%d,lines=%s' % (i, p, c))

    # ---- [GEO] a stab-i point never lies on a V4-fixed line A_j with j != i,
    #      and lies on A_i whenever A_i is present.  Rendered abstractly:
    #      a V4-fixed line's point row is a set of pair points of ONE index,
    #      containing ALL of them.
    for k in Vlns:
        idxs = set()
        for p in lsets[k]:
            s = pstab[p]
            if len(s) == 2:
                idxs.add(next(iter(s - {0})))
            elif s == FULL:
                bad.append('GEO_vertex_on_axis:line=%d,pt=%d' % (k, p))
        if len(idxs) > 1:
            bad.append('GEO_axis_mixed_index:line=%d,idx=%s' % (k, sorted(idxs)))
        elif len(idxs) == 1:
            m = idxs.pop()
            if set(Pi[m]) != set(lsets[k]):
                bad.append('GEO_axis_not_all_stab_pts:line=%d,m=%d' % (k, m))

    # ---- [GEO] dual of the previous: a vertex's pencil is ALL stab-m lines
    #      for one index m and nothing else.
    for p in Vpts:
        thru = [k for k in range(len(lsets)) if p in lsets[k]]
        idxs = set()
        for k in thru:
            s = lstab[k]
            if len(s) == 2:
                idxs.add(next(iter(s - {0})))
            elif s == FULL:
                pass  # counted above as GEO_vertex_on_axis
            else:
                bad.append('GEO_vertex_on_freeline2:pt=%d,line=%d' % (p, k))
        if len(idxs) > 1:
            bad.append('GEO_pencil_mixed_index:pt=%d,idx=%s' % (p, sorted(idxs)))
        elif len(idxs) == 1:
            m = idxs.pop()
            if set(Li[m]) - set(thru):
                bad.append('GEO_pencil_not_all_stab_lines:pt=%d,m=%d' % (p, m))

    if require_frame:
        # ---- [GEO] Theorem A: exactly one vertex and one axis
        if len(Vpts) != 1 or len(Vlns) != 1:
            bad.append('GEO_ThmA_frame:f=%d,fstar=%d' % (len(Vpts), len(Vlns)))
        else:
            x, K = Vpts[0], Vlns[0]
            if x in lsets[K]:
                bad.append('GEO_ThmA_vertex_on_own_axis')
            ms = {next(iter(pstab[p] - {0})) for p in lsets[K] if len(pstab[p]) == 2}
            mls = {next(iter(lstab[k] - {0})) for k in range(len(lsets))
                   if x in lsets[k] and len(lstab[k]) == 2}
            if len(ms) == 1 and len(mls) == 1 and ms != mls:
                bad.append('GEO_ThmA_index_mismatch:axis=%s,vertex=%s'
                           % (sorted(ms), sorted(mls)))
    return bad


# ----------------------------------------------------------------------
# 4.  independent canonical form (individualisation-refinement)
# ----------------------------------------------------------------------
#
# Deliberately different from the sidecar's:
#   - seeded with the QUADRILATERAL count (number of 8-cycles of the Levi
#     graph through each vertex), not the triangle/6-cycle count;
#   - target cell = the FIRST non-singleton colour class in colour order,
#     not the smallest;
#   - leaf encoding = the sorted tuple of canonical line point-sets,
#     prefixed by the role word, not a packed adjacency bitmatrix.
# The canonical form is exact for ANY choice of these (the tree is searched
# exhaustively and the minimum over leaves is taken); the differences are
# there so that the two implementations are not co-buggy.

def _levi(n, lines):
    adj = [[] for _ in range(2 * n)]
    for i, l in enumerate(lines):
        for p in l:
            adj[p].append(n + i)
            adj[n + i].append(p)
    return adj


def _quad_counts(n, lines, adj):
    """8-cycles of the Levi graph through each vertex.  For a linear space
    an 8-cycle is p1 l1 p2 l2 p3 l3 p4 l4 with all p, l distinct: a
    'quadrilateral'.  Counted by brute force over pairs of points at Levi
    distance 2 -- cheap at n = 23."""
    nv = 2 * n
    # co-neighbour multiplicity graph at distance 2 (points<->points via
    # lines, lines<->lines via points); in a linear space each such pair is
    # joined by exactly one 2-path, so the count of 4-cycles in this
    # "distance-2" graph gives the 8-cycles of the Levi graph.
    d2 = [set() for _ in range(nv)]
    for v in range(nv):
        for w in adj[v]:
            for u in adj[w]:
                if u != v:
                    d2[v].add(u)
    cnt = [0] * nv
    for v in range(nv):
        nb = sorted(d2[v])
        for x, y in itertools.combinations(nb, 2):
            # 4-cycles v - x - ? - y - v in the distance-2 graph
            common = len((d2[x] & d2[y]) - {v})
            cnt[v] += common
    return cnt


def _refine(adj, colour):
    nv = len(adj)
    colour = list(colour)
    while True:
        sig = [(colour[v], tuple(sorted(colour[w] for w in adj[v]))) for v in range(nv)]
        order = sorted(set(sig))
        rank = {s: i for i, s in enumerate(order)}
        new = [rank[s] for s in sig]
        if new == colour:
            return new
        colour = new


def _leaf_encoding(n, lines, colour):
    """colour is discrete: colour[v] is the canonical rank of v."""
    nv = 2 * n
    rank = colour
    # role word: bit i set iff canonical position i is a POINT
    role = 0
    for v in range(nv):
        if v < n:
            role |= 1 << rank[v]
    rows = []
    for i, l in enumerate(lines):
        rows.append((rank[n + i], tuple(sorted(rank[p] for p in l))))
    rows.sort()
    return (role, tuple(r[1] for r in rows))


def _canon_search(n, lines, adj, colour, best, bestlab):
    colour = _refine(adj, colour)
    nv = len(adj)
    cells = defaultdict(list)
    for v in range(nv):
        cells[colour[v]].append(v)
    target = None
    for c in sorted(cells):                 # FIRST non-singleton, by colour
        if len(cells[c]) > 1:
            target = cells[c]
            break
    if target is None:
        enc = _leaf_encoding(n, lines, colour)
        if best[0] is None or enc < best[0]:
            best[0] = enc
            bestlab[0] = tuple(colour)
        return
    nc = max(colour) + 1
    for v in target:
        c2 = list(colour)
        c2[v] = nc
        _canon_search(n, lines, adj, c2, best, bestlab)


def canonical(n, lines):
    """Returns (encoding, canonical_labelling).  Two structures have equal
    encodings iff they are isomorphic by a role-preserving isomorphism."""
    lines = [tuple(sorted(l)) for l in lines]
    adj = _levi(n, lines)
    q = _quad_counts(n, lines, adj)
    seed = [(0 if v < n else 1, q[v]) for v in range(2 * n)]
    order = sorted(set(seed))
    rank = {s: i for i, s in enumerate(order)}
    colour = [rank[s] for s in seed]
    best = [None]
    bestlab = [None]
    _canon_search(n, lines, adj, colour, best, bestlab)
    return best[0], bestlab[0]


def canon_key(n, lines):
    return canonical(n, lines)[0]


def canon_hex(n, lines):
    enc = canon_key(n, lines)
    s = repr(enc).encode()
    return hashlib.sha256(b'av4|%d|' % n + s).hexdigest()


def dual_lines(n, lines):
    d = [[] for _ in range(n)]
    for i, l in enumerate(lines):
        for p in l:
            d[p].append(i)
    return [tuple(sorted(x)) for x in d]


# ----------------------------------------------------------------------
# 5.  explicit isomorphism certificate (used to certify class integrity)
# ----------------------------------------------------------------------

def relabel(n, lines, perm):
    """perm: point label -> new point label"""
    return sorted(tuple(sorted(perm[p] for p in l)) for l in lines)


def iso_from_canonical(n, linesA, linesB):
    """If canonical(A) == canonical(B), return an explicit point bijection
    pi with relabel(A, pi) == sorted(B); else None.  The returned map is
    VERIFIED before it is returned."""
    ea, la = canonical(n, linesA)
    eb, lb = canonical(n, linesB)
    if ea != eb:
        return None
    # la[v] = canonical rank of v in A (v < n : points).  Same for B.
    posB = {}
    for v in range(2 * n):
        posB[lb[v]] = v
    pi = {}
    for p in range(n):
        w = posB[la[p]]
        if w >= n:
            return None
        pi[p] = w
    if relabel(n, linesA, pi) != sorted(tuple(sorted(l)) for l in linesB):
        return None
    return pi
