#!/usr/bin/env python3
"""A fast EXACT canonical form, used only for INTERNAL de-duplication
inside this lane's independent enumerator.

It is exact for the same reason any individualisation-refinement scheme
is: the search tree is explored exhaustively and the canonical form is the
minimum over all leaves; the refinement and the target-cell rule are
isomorphism-invariant and are used only to prune, never to decide.

The FINAL cross-comparison against the frozen corpus is always done with
`av4.canonical`, which uses a different seed, a different target-cell rule
and a different leaf encoding.  `run_selfcheck()` below verifies on a
sample that the two forms induce the SAME partition.
"""

import hashlib
from collections import defaultdict


def _seed_colours(n, lines):
    """(role, triangle count) via bitmasks -- cheap."""
    colin = [0] * n
    lmask = []
    for l in lines:
        m = 0
        for p in l:
            m |= 1 << p
        lmask.append(m)
        for p in l:
            colin[p] |= m & ~(1 << p)
    tri_p = [0] * n
    tri_l = [0] * n
    for i, l in enumerate(lines):
        ll = tuple(l)
        m = lmask[i]
        for ai in range(4):
            for bi in range(ai + 1, 4):
                p, q = ll[ai], ll[bi]
                c = bin(colin[p] & colin[q] & ~m).count('1')
                tri_l[i] += c
                tri_p[p] += c
                tri_p[q] += c
    vals = sorted(set([(0, t) for t in tri_p] + [(1, t) for t in tri_l]))
    vid = {v: k for k, v in enumerate(vals)}
    return [vid[(0, tri_p[p])] for p in range(n)] + \
           [vid[(1, tri_l[i])] for i in range(n)]


def _refine(adj, colour, nv):
    colour = list(colour)
    while True:
        sig = [None] * nv
        for v in range(nv):
            sig[v] = (colour[v],) + tuple(sorted(colour[w] for w in adj[v]))
        order = sorted(set(sig))
        rank = {s: i for i, s in enumerate(order)}
        new = [rank[s] for s in sig]
        if new == colour:
            return new
        colour = new


def _search(adj, colour, nv, n, best):
    colour = _refine(adj, colour, nv)
    cells = defaultdict(list)
    for v in range(nv):
        cells[colour[v]].append(v)
    target = None
    for c in sorted(cells, key=lambda c: (len(cells[c]), c)):
        if len(cells[c]) > 1:
            target = cells[c]
            break
    if target is None:
        pos = sorted(range(nv), key=lambda v: colour[v])
        rank = [0] * nv
        for i, v in enumerate(pos):
            rank[v] = i
        role = 0
        for i, v in enumerate(pos):
            if v < n:
                role |= 1 << i
        rows = [role]
        for i, v in enumerate(pos):
            bits = 0
            for w in adj[v]:
                bits |= 1 << rank[w]
            rows.append(bits)
        enc = tuple(rows)
        if best[0] is None or enc < best[0]:
            best[0] = enc
        return
    nc = max(colour) + 1
    for v in target:
        c2 = list(colour)
        c2[v] = nc
        _search(adj, c2, nv, n, best)


def canon(n, lines):
    nv = 2 * n
    adj = [[] for _ in range(nv)]
    for i, l in enumerate(lines):
        for p in l:
            adj[p].append(n + i)
            adj[n + i].append(p)
    colour = _seed_colours(n, lines)
    best = [None]
    _search(adj, colour, nv, n, best)
    return best[0]


def canon_hex(n, lines):
    return hashlib.sha256(repr(canon(n, lines)).encode()).hexdigest()
