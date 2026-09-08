#!/usr/bin/env python3
"""Packet item 5: exhaustive bounded control on a SMALLER orbit profile.

Target profile: the exact structural analogue of the n = 23 frame at
n = 15 --  f = f* = 1, b_1 = b*_1 = 2, (b_2,b_3) = (0,1),
(b*_2,b*_3) = (0,1), a = a* = 2.  (Theorem A and Theorem B hold verbatim
for every odd n with n - 9 not divisible by 4; Corollary D1 leaves exactly
the analogous "b = b* = 1" cells at n = 15.)

Two enumerations are compared:

  (BF) a COMPLETELY UNNORMALISED brute force: every V4-invariant set of
       line orbits on the fixed labelled point system whose union is an
       (n_4) linear space.  No frame is forced, no orderly rule, no gauge
       fixing -- only "a set of orbits is a set", encoded by listing the
       orbits in increasing representative order.  This is exhaustive by
       construction and needs no completeness argument at all.

  (NA) the same normalisation and the same prunes as
       `indep_enum.py` (Proposition N-A of ../PROOFS.md).

The control checks
  * set equality of the resulting bare types,
  * set equality of the FENCE-VALID subsets,
  * MULTIPLICITY: for every type, the number of unnormalised labelled
    realisations, and that this equals |Gamma| / |stabiliser| for the
    explicitly constructed relabelling group Gamma,
  * and it quantifies the abstract-vs-geometric separation at n = 15.
"""

import itertools
import json
import os
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import av4          # noqa: E402
import fastcanon    # noqa: E402

V4 = (0, 1, 2, 3)
NONTRIV = (1, 2, 3)


class Sys:
    def __init__(self, n, pair_idx, a):
        self.n = n
        self.pair_idx = list(pair_idx)
        self.a = a
        self.FB = 1 + 2 * len(pair_idx)
        assert self.FB + 4 * a == n
        perms = [list(range(n)) for _ in V4]
        for g in NONTRIV:
            P = perms[g]
            for t, i in enumerate(self.pair_idx):
                u = 1 + 2 * t
                if g != i:
                    P[u], P[u + 1] = u + 1, u
            for o in range(a):
                B = self.FB + 4 * o
                for h in V4:
                    P[B + h] = B + (g ^ h)
        self.perms = tuple(tuple(p) for p in perms)
        self.kind = []
        for p in range(n):
            if p == 0:
                self.kind.append(('x', None, None))
            elif p < self.FB:
                t = (p - 1) // 2
                self.kind.append(('pair', self.pair_idx[t], t))
            else:
                o = (p - self.FB) // 4
                self.kind.append(('free', o, (p - self.FB) % 4))

    def orbit(self, S):
        out = []
        for g in V4:
            T = frozenset(self.perms[g][p] for p in S)
            if T not in out:
                out.append(T)
        return out

    def gamma(self):
        """the full V4-equivariant relabelling group (explicitly built)"""
        groups = defaultdict(list)
        for t, i in enumerate(self.pair_idx):
            groups[i].append(1 + 2 * t)
        perms = [tuple(range(self.n))]

        def mult(fac):
            nonlocal perms
            perms = [tuple(f[b[p]] for p in range(self.n))
                     for b in perms for f in fac]
        for i in sorted(groups):
            bases = groups[i]
            k = len(bases)
            fac = []
            for sigma in itertools.permutations(range(k)):
                for bits in itertools.product((0, 1), repeat=k):
                    f = list(range(self.n))
                    for ai, b_ in enumerate(bases):
                        tb = bases[sigma[ai]]
                        f[b_] = tb + bits[ai]
                        f[b_ + 1] = tb + 1 - bits[ai]
                    fac.append(f)
            mult(fac)
        if self.a:
            fac = []
            for sigma in itertools.permutations(range(self.a)):
                for us in itertools.product(V4, repeat=self.a):
                    f = list(range(self.n))
                    for o in range(self.a):
                        B, TB = self.FB + 4 * o, self.FB + 4 * sigma[o]
                        for h in V4:
                            f[B + h] = TB + (h ^ us[o])
                    fac.append(f)
            mult(fac)
        return perms


def all_orbits(sysm):
    """Every V4-orbit of 4-subsets, keyed by its lexicographically least
    representative; no filtering whatsoever."""
    n = sysm.n
    seen = {}
    for S in itertools.combinations(range(n), 4):
        Sf = frozenset(S)
        orb = sysm.orbit(Sf)
        rep = min(tuple(sorted(T)) for T in orb)
        if rep in seen:
            continue
        seen[rep] = [tuple(sorted(T)) for T in orb]
    return seen


def brute_force(sysm):
    """Exhaustive, unnormalised.  Returns {canonical key: [labelled line
    tuples]} and per-key counts."""
    n = sysm.n
    orbs = all_orbits(sysm)
    keys = sorted(orbs)
    sizes = [len(orbs[k]) for k in keys]
    out = defaultdict(list)
    nleaf = 0
    lines = []
    deg = [0] * n
    adj = [0] * n

    def rec(start, nl):
        nonlocal nleaf
        if nl == n:
            if all(d == 4 for d in deg):
                nleaf += 1
                out['__leaf__'].append(tuple(sorted(lines)))
            return
        if nl > n:
            return
        for idx in range(start, len(keys)):
            k = keys[idx]
            orb = orbs[k]
            if nl + len(orb) > n:
                continue
            add = Counter()
            for L in orb:
                for p in L:
                    add[p] += 1
            if any(deg[p] + c > 4 for p, c in add.items()):
                continue
            ok = True
            applied = []
            for L in orb:
                m = 0
                for p in L:
                    m |= 1 << p
                bad = False
                for p in L:
                    if adj[p] & (m & ~(1 << p)):
                        bad = True
                        break
                if bad:
                    ok = False
                    break
                for p in L:
                    adj[p] |= m & ~(1 << p)
                applied.append((L, m))
            if not ok:
                for L, m in applied:
                    for p in L:
                        adj[p] &= ~(m & ~(1 << p))
                continue
            for p, c in add.items():
                deg[p] += c
            lines.extend(orb)
            rec(idx + 1, nl + len(orb))
            del lines[-len(orb):]
            for p, c in add.items():
                deg[p] -= c
            for L, m in applied:
                for p in L:
                    adj[p] &= ~(m & ~(1 << p))
            # rebuild adj exactly (cheap at this size)
            for p in range(n):
                adj[p] = 0
            for L in lines:
                m = 0
                for p in L:
                    m |= 1 << p
                for p in L:
                    adj[p] |= m & ~(1 << p)
    rec(0, 0)
    return out['__leaf__']


def normalised(sysm, b2, b3, bs2, bs3, prunes=('bad', 'omin')):
    """The N-A enumerator, same rules as indep_enum.py, at general n.
    `prunes` selects which OPTIONAL prunes are active, so that a
    premature-prune adversary can switch them off one at a time."""
    n = sysm.n
    FB = sysm.FB
    if sysm.a < 2:
        # Proposition N-A needs a >= 2; Corollary D1 proves a >= 2 for every
        # nonempty cell, so a < 2 cells are empty by proof.
        return []
    astar = (n - 5 - 2 * (bs2 + bs3)) // 4
    slots = [('axis', None), ('L1', 1), ('L1', 1)] + \
            [('M', 2)] * bs2 + [('M', 3)] * bs3 + [('G', None)] * astar
    forced = {0: [(1, 2, 3, 4)], 1: [(0, 1, FB, FB + 1)],
              2: [(0, 3, FB + 4, FB + 5)]}
    omin = [min(sysm.perms[g][p] for g in V4) for p in range(n)]
    out = []
    state = {'adj': [0] * n, 'deg': [0] * n, 'lines': []}

    def gen_M(i):
        res = []
        for o1 in range(sysm.a):
            for o2 in range(o1 + 1, sysm.a):
                for h2 in (0, 1):
                    c1 = (FB + 4 * o1, FB + 4 * o1 + i)
                    c2 = (FB + 4 * o2 + h2, FB + 4 * o2 + (h2 ^ i))
                    res.append(tuple(sorted(c1 + c2)))
        return sorted(set(res))

    def gen_G(prev):
        adj, deg = state['adj'], state['deg']
        bad = list(adj)
        for g in NONTRIV:
            P = sysm.perms[g]
            for p in range(n):
                m = adj[P[p]]
                bb = 0
                while m:
                    low = m & -m
                    bb |= 1 << P[low.bit_length() - 1]
                    m ^= low
                bad[p] |= bb
        pts = []
        for p in range(n):
            k = sysm.kind[p][0]
            if k == 'x':
                continue
            need = 2 if k == 'pair' else 1
            if deg[p] + need <= 4:
                pts.append(p)
        res, cur, mask = [], [], [0]
        prevt = prev if prev is not None else ()

        def dfs(start, uf, us, tight):
            d = len(cur)
            if d == 4:
                res.append(tuple(cur))
                return
            for idx in range(start, len(pts)):
                p = pts[idx]
                if d == 0:
                    if 'omin' in prunes and omin[p] != p:
                        continue
                else:
                    if 'omin' in prunes and omin[p] < cur[0]:
                        continue
                    if 'bad' in prunes and (bad[p] & mask[0]):
                        continue
                t2 = tight
                if tight and d < len(prevt):
                    if p < prevt[d]:
                        continue
                    if p > prevt[d]:
                        t2 = False
                    elif d == 3:
                        continue
                k, i, _ = sysm.kind[p]
                if k == 'free':
                    if i in uf:
                        continue
                    cur.append(p); mask[0] |= 1 << p
                    dfs(idx + 1, uf | {i}, us, t2)
                    cur.pop(); mask[0] &= ~(1 << p)
                else:
                    if i in us:
                        continue
                    cur.append(p); mask[0] |= 1 << p
                    dfs(idx + 1, uf, us | {i}, t2)
                    cur.pop(); mask[0] &= ~(1 << p)
        dfs(0, frozenset(), frozenset(), prev is not None)
        return res

    def place(S, kind, stab):
        Sf = frozenset(S)
        orb = sysm.orbit(Sf)
        if kind == 'axis' and len(orb) != 1:
            return None
        if kind in ('L1', 'M'):
            if len(orb) != 2 or frozenset(sysm.perms[stab][p] for p in Sf) != Sf:
                return None
        if kind == 'G':
            if len(orb) != 4:
                return None
            if tuple(sorted(Sf)) != min(tuple(sorted(T)) for T in orb):
                return None
        adj, deg = state['adj'], state['deg']
        add = Counter()
        for L in orb:
            for p in L:
                add[p] += 1
        if any(deg[p] + c > 4 for p, c in add.items()):
            return None
        applied = []
        for L in orb:
            m = 0
            for p in L:
                m |= 1 << p
            if any(adj[p] & (m & ~(1 << p)) for p in L):
                for L2, m2 in applied:
                    for p in L2:
                        adj[p] &= ~(m2 & ~(1 << p))
                return None
            for p in L:
                adj[p] |= m & ~(1 << p)
            applied.append((L, m))
        for p, c in add.items():
            deg[p] += c
        state['lines'].extend(tuple(sorted(L)) for L in orb)
        return (applied, add)

    def unplace(tok):
        applied, add = tok
        adj, deg = state['adj'], state['deg']
        del state['lines'][-len(applied):]
        for p, c in add.items():
            deg[p] -= c
        for p in range(n):
            adj[p] = 0
        for L in state['lines']:
            m = 0
            for p in L:
                m |= 1 << p
            for p in L:
                adj[p] |= m & ~(1 << p)

    def rec(si, prev_by_type):
        if si == len(slots):
            if all(d == 4 for d in state['deg']):
                out.append(tuple(sorted(state['lines'])))
            return
        kind, stab = slots[si]
        key = (kind, stab)
        prev = prev_by_type.get(key)
        if si in forced:
            cands = [S for S in forced[si] if prev is None or S > prev]
        elif kind == 'M':
            cands = [S for S in gen_M(stab) if prev is None or S > prev]
        else:
            cands = gen_G(prev)
        for S in cands:
            tok = place(S, kind, stab)
            if tok is None:
                continue
            old = prev_by_type.get(key)
            prev_by_type[key] = tuple(S)
            rec(si + 1, prev_by_type)
            if old is None:
                del prev_by_type[key]
            else:
                prev_by_type[key] = old
            unplace(tok)
    rec(0, {})
    return out


def one_profile(n, b2, b3, bs2, bs3, label):
    t0 = time.time()
    a = (n - 5 - 2 * (b2 + b3)) // 4
    sysm = Sys(n, [1, 1] + [2] * b2 + [3] * b3, a)

    bf = brute_force(sysm)
    bf_keys = Counter()
    bf_fence = Counter()
    bf_reps = {}
    for lines in bf:
        k = fastcanon.canon(n, list(lines))
        bf_keys[k] += 1
        bf_reps.setdefault(k, lines)
        nec = av4.necessary_conditions(n, [frozenset(l) for l in lines], sysm.perms)
        if not nec:
            bf_fence[k] += 1

    na = normalised(sysm, b2, b3, bs2, bs3)
    na_keys = Counter()
    for lines in na:
        na_keys[fastcanon.canon(n, list(lines))] += 1

    # A4 premature-prune adversary: switch each optional prune off
    prune_variants = {}
    for pr in (('bad',), ('omin',), ()):
        v = normalised(sysm, b2, b3, bs2, bs3, prunes=pr)
        prune_variants['prunes=%s' % (pr,)] = {
            'labelled': len(v),
            'types': len({fastcanon.canon(n, list(l)) for l in v}),
            'same_type_set': {fastcanon.canon(n, list(l)) for l in v} == set(na_keys),
        }

    # multiplicity check: |Gamma-orbit| of each labelled structure
    G = sysm.gamma()
    mult = {}
    for k, rep in bf_reps.items():
        images = set()
        for gm in G:
            images.add(tuple(sorted(tuple(sorted(gm[p] for p in l)) for l in rep)))
        mult[k] = len(images)

    fenceset = {k for k, v in bf_fence.items() if v > 0}
    # every brute-force labelled structure of a fence-valid type must itself
    # be fence-valid (the conditions are Gamma-invariant)
    fence_consistent = all(bf_fence[k] in (0, bf_keys[k]) for k in bf_keys)

    res = {
        'profile': {'n': n, 'pair_idx': sysm.pair_idx, 'a': sysm.a,
                    'cell': label},
        'brute_force_labelled_structures': len(bf),
        'brute_force_bare_types': len(bf_keys),
        'brute_force_fence_valid_types': len(fenceset),
        'fence_validity_is_type_level': fence_consistent,
        'normalised_labelled_structures': len(na),
        'normalised_bare_types': len(na_keys),
        'gamma_order': len(G),
        'SET_EQUALITY_normalised_vs_bruteforce_fencevalid':
            set(na_keys) == fenceset,
        'normalised_output_all_fence_valid': set(na_keys) <= fenceset,
        'missing_from_normalised': len(fenceset - set(na_keys)),
        'extra_in_normalised': len(set(na_keys) - fenceset),
        'MULTIPLICITY_gamma_orbit_equals_bruteforce_count':
            all(mult[k] == bf_keys[k] for k in bf_keys),
        'multiplicity_table': sorted(
            [[bf_keys[k], mult[k], bf_fence[k], len(bf_reps)] for k in bf_keys])[:6],
        'A4_premature_prune_variants': prune_variants,
        'abstract_vs_geometric_separation': {
            'types_satisfying_only_the_abstract_axioms':
                len(bf_keys) - len(fenceset),
            'types_also_fence_valid': len(fenceset),
        },
        'seconds': round(time.time() - t0, 1),
    }
    return res


def main():
    profiles = [
        (15, 0, 1, 0, 1, 'n15-b01-bs01  (analogue of the n=23 frame)'),
        (15, 0, 3, 0, 1, 'n15-b03-bs01  (a=1: proved EMPTY by Corollary D1)'),
        (19, 0, 1, 0, 1, 'n19-b01-bs01  (a=a*=3)'),
    ]
    if len(sys.argv) > 1:
        profiles = [p for p in profiles if sys.argv[1] in p[5]]
    out = []
    for n, b2, b3, bs2, bs3, label in profiles:
        print('### %s' % label, flush=True)
        r = one_profile(n, b2, b3, bs2, bs3, label)
        print(json.dumps(r, indent=1, default=str), flush=True)
        out.append(r)
    d = os.path.join(os.path.dirname(HERE), 'output')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'item5_small_controls.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=str)


if __name__ == '__main__':
    main()
