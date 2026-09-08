#!/usr/bin/env python3
"""INDEPENDENT enumerator for V4-equivariant fence-valid (23_4) types.

Packet item 3, second direction ("every abstract coherent action satisfying
the necessary conditions is represented ... before canonical quotienting")
and item 5.  Written against this lane's own derivation (../PROOFS.md);
it shares no code with the sidecar's `v4census.py`.

WHAT IS ASSUMED (each item proved in ../PROOFS.md, and machine-checked in
`theory_checks.py`):
  T-A  exactly one vertex x, exactly one axis L, same index (WLOG index 1),
       b_1 = b*_1 = 2;
  T-B1 L's point row is exactly the four stab-1 points;
       x's line pencil is exactly the four stab-1 lines;
  T-B2 the two P_1 orbits and two L_1 orbits are matched bijectively, each
       P_1 point additionally on exactly one free-line class, and each L_1
       line additionally carrying exactly one free-point class;
  T-B3 for i in {2,3}: P_i orbits meet no L_i line; each L_i orbit carries
       exactly two free-point classes; each P_i orbit lies on exactly two
       free-line classes;
  L-D  (free-orbit separation) two DISTINCT line orbits with the SAME
       stabiliser index have disjoint free-point neighbourhoods.

NORMALISATION (the only relabelling normalisation used; proved in
../PROOFS.md sec.9 as `Normalisation N-A`):
  points  0 = x; stab-1 pairs {1,2} and {3,4}; then stab-2 pairs, stab-3
  pairs; then the free orbits in blocks of four, F_o = {FB+4o+h}.
  The two L_1 orbit representatives are FORCED to
      {0, 1, FB+0, FB+1}    and    {0, 3, FB+4, FB+5}.
  NOTHING else is normalised: no orderly/`Gamma`-minimality rule is used
  anywhere, so no completeness argument beyond N-A is needed.  All residual
  relabelling duplication is removed at the leaves by an exact canonical
  form.

Every other restriction applied in the search is a NECESSARY condition
(orbit size, the linear-space pair condition, degree caps, feasibility
bounds, lexicographic ordering of interchangeable same-type slots, and the
choice of the lexicographically least representative of each line orbit).
"""

import argparse
import itertools
import json
import os
import sys
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import av4          # noqa: E402
import fastcanon    # noqa: E402

V4 = (0, 1, 2, 3)
NONTRIV = (1, 2, 3)


class Cell:
    def __init__(self, b2, b3, bs2, bs3):
        self.b2, self.b3, self.bs2, self.bs3 = b2, b3, bs2, bs3
        self.b = b2 + b3
        self.bs = bs2 + bs3
        assert (18 - 2 * self.b) % 4 == 0 and (18 - 2 * self.bs) % 4 == 0
        self.a = (18 - 2 * self.b) // 4
        self.astar = (18 - 2 * self.bs) // 4
        self.n = 23
        self.pair_idx = [1, 1] + [2] * b2 + [3] * b3
        self.T = len(self.pair_idx)
        self.FB = 1 + 2 * self.T
        assert self.FB + 4 * self.a == 23, (self.FB, self.a)
        # V4 action on points
        perms = [list(range(23)) for _ in V4]
        for g in NONTRIV:
            P = perms[g]
            for t, i in enumerate(self.pair_idx):
                u = 1 + 2 * t
                if g != i:
                    P[u], P[u + 1] = u + 1, u
            for o in range(self.a):
                B = self.FB + 4 * o
                for h in V4:
                    P[B + h] = B + (g ^ h)
        self.perms = tuple(tuple(p) for p in perms)
        self.kind = []
        for p in range(23):
            if p == 0:
                self.kind.append(('x', None, None))
            elif p < self.FB:
                t = (p - 1) // 2
                self.kind.append(('pair', self.pair_idx[t], t))
            else:
                o = (p - self.FB) // 4
                self.kind.append(('free', o, (p - self.FB) % 4))
        self.orbitmin = [min(self.perms[g][p] for g in V4) for p in range(23)]

    @property
    def name(self):
        return 'n23-fence-b%d%d-bs%d%d' % (self.b2, self.b3, self.bs2, self.bs3)

    def free(self, o, h):
        return self.FB + 4 * o + h

    def act(self, g, S):
        P = self.perms[g]
        return frozenset(P[p] for p in S)

    def orbit(self, S):
        out = []
        for g in V4:
            T = self.act(g, S)
            if T not in out:
                out.append(T)
        return out


def admissible(cell):
    """The cell-level necessary conditions proved in ../PROOFS.md
    (Lemma D corollaries).  Returns [] if the cell may be nonempty."""
    why = []
    if cell.a < 2:
        why.append('a<2')
    if cell.astar < 2:
        why.append('astar<2')
    for i, bi in ((2, cell.b2), (3, cell.b3)):
        if 2 * bi > cell.astar:
            why.append('2b%d>astar' % i)
    for i, bi in ((2, cell.bs2), (3, cell.bs3)):
        if 2 * bi > cell.a:
            why.append('2bs%d>a' % i)
    return why


class Enum:
    def __init__(self, cell, use_cell_admissibility=True, collect=True,
                 deadline=None, shard=None):
        # `shard = (slot_index, j)` restricts slot `slot_index` to its j-th
        # candidate.  Sharding partitions the search tree at one level, so
        # the union over all j of the shards is exactly the unsharded run;
        # it is a scheduling device only, with no effect on completeness.
        self.c = cell
        self.collect = collect
        self.deadline = deadline
        self.shard = shard
        self.leaves = 0
        self.nodes = 0
        self.types = {}
        self.truncated = False
        self.t0 = time.monotonic()
        self.rej = defaultdict(int)
        c = cell
        self.slots = [('axis', None)] + [('L1', 1), ('L1', 1)] + \
                     [('M', 2)] * c.bs2 + [('M', 3)] * c.bs3 + \
                     [('G', None)] * c.astar
        assert 1 + 2 * 2 + 2 * (c.bs2 + c.bs3) + 4 * c.astar == 23
        self.forced = {
            0: [(1, 2, 3, 4)],
            1: [(0, 1, c.FB, c.FB + 1)],
            2: [(0, 3, c.FB + 4, c.FB + 5)],
        }
        self.suffix_G = [0] * (len(self.slots) + 1)
        self.suffix_M = [0] * (len(self.slots) + 1)
        for k in range(len(self.slots) - 1, -1, -1):
            self.suffix_G[k] = self.suffix_G[k + 1] + (self.slots[k][0] == 'G')
            self.suffix_M[k] = self.suffix_M[k + 1] + (self.slots[k][0] in ('M', 'L1'))

    # -------- candidate generators -------------------------------------
    def gen_M(self, i):
        """A stab-i line orbit (i in {2,3}) consists of two lines, each
        carrying one <s_i>-coset from each of TWO distinct free point
        orbits (T-B3 + row 9).  The lexicographically least representative
        of the orbit necessarily carries the coset of the LOWER orbit that
        contains index 0, so h1 = 0; h2 ranges over both cosets."""
        c = self.c
        out = []
        for o1 in range(c.a):
            for o2 in range(o1 + 1, c.a):
                for h2 in (0, 1):
                    c1 = (c.free(o1, 0), c.free(o1, i))
                    c2 = (c.free(o2, h2), c.free(o2, h2 ^ i))
                    S = tuple(sorted(c1 + c2))
                    if len(set(S)) == 4:
                        out.append(S)
        return sorted(set(out))

    def gen_G(self, state, prev):
        """Free line orbit representatives.  Necessary conditions only."""
        c = self.c
        deg = state['deg']
        adj = state['adj']
        omin = c.orbitmin
        # symmetrised conflict mask
        bad = list(adj)
        for g in NONTRIV:
            P = c.perms[g]
            for p in range(23):
                m = adj[P[p]]
                if m:
                    bb = 0
                    while m:
                        low = m & -m
                        bb |= 1 << P[low.bit_length() - 1]
                        m ^= low
                    bad[p] |= bb
        pts = []
        for p in range(23):
            k = c.kind[p][0]
            if k == 'x':
                continue                       # T-A: no vertex on a free line
            need = 2 if k == 'pair' else 1
            if deg[p] + need <= 4:
                pts.append(p)
        out = []
        cur = []
        mask = [0]
        prevt = prev if prev is not None else ()

        def dfs(start, used_free, used_stab, tight):
            d = len(cur)
            if d == 4:
                out.append(tuple(cur))
                return
            for idx in range(start, len(pts)):
                p = pts[idx]
                if d == 0:
                    if omin[p] != p:
                        continue
                else:
                    if omin[p] < cur[0]:
                        continue
                    if bad[p] & mask[0]:
                        continue
                t2 = tight
                if tight and d < len(prevt):
                    if p < prevt[d]:
                        continue
                    if p > prevt[d]:
                        t2 = False
                    elif d == 3:
                        continue
                k, i, _ = c.kind[p]
                if k == 'free':
                    if i in used_free:
                        continue
                    cur.append(p); mask[0] |= 1 << p
                    dfs(idx + 1, used_free | {i}, used_stab, t2)
                    cur.pop(); mask[0] &= ~(1 << p)
                else:
                    if i in used_stab:
                        continue
                    cur.append(p); mask[0] |= 1 << p
                    dfs(idx + 1, used_free, used_stab | {i}, t2)
                    cur.pop(); mask[0] &= ~(1 << p)
        dfs(0, frozenset(), frozenset(), prev is not None)
        return out

    # -------- placement ------------------------------------------------
    def place(self, S, kind, stab, state):
        c = self.c
        Sf = frozenset(S)
        orb = c.orbit(Sf)
        if kind == 'axis':
            if len(orb) != 1:
                self.rej['stab'] += 1
                return None
        elif kind in ('L1', 'M'):
            if len(orb) != 2 or c.act(stab, Sf) != Sf:
                self.rej['stab'] += 1
                return None
        else:
            if len(orb) != 4:
                self.rej['stab'] += 1
                return None
            if tuple(sorted(Sf)) != min(tuple(sorted(T)) for T in orb):
                self.rej['notlexmin'] += 1
                return None
        adj, deg = state['adj'], state['deg']
        add = defaultdict(int)
        for L in orb:
            for p in L:
                add[p] += 1
        for p, d in add.items():
            if deg[p] + d > 4:
                self.rej['deg'] += 1
                return None
        masks = []
        for L in orb:
            m = 0
            for p in L:
                m |= 1 << p
            masks.append((L, m))
        # pair condition, including within the new orbit
        applied = []
        for L, m in masks:
            hit = False
            for p in L:
                if adj[p] & (m & ~(1 << p)):
                    hit = True
                    break
            if hit:
                for L2, m2 in applied:
                    for p in L2:
                        adj[p] &= ~(m2 & ~(1 << p))
                self.rej['pair'] += 1
                return None
            for p in L:
                adj[p] |= m & ~(1 << p)
            applied.append((L, m))
        for p, d in add.items():
            deg[p] += d
        state['lines'].extend(tuple(sorted(L)) for L in orb)
        return (masks, add)

    def unplace(self, token, state):
        masks, add = token
        adj, deg = state['adj'], state['deg']
        del state['lines'][-len(masks):]
        for p, d in add.items():
            deg[p] -= d
        for p in range(23):
            adj[p] = 0
        for L in state['lines']:
            m = 0
            for p in L:
                m |= 1 << p
            for p in L:
                adj[p] |= m & ~(1 << p)

    def feasible(self, si, state):
        """Necessary feasibility bound.  Per remaining slot, an upper bound
        on the degree a point can still gain:
            free-line orbit : pair point 2, free point 1, vertex 0 (T-A)
            stab-line orbit : pair point 1, free point 1, vertex 2"""
        deg = state['deg']
        nG, nM = self.suffix_G[si], self.suffix_M[si]
        for p in range(23):
            d = 4 - deg[p]
            if d <= 0:
                continue
            k = self.c.kind[p][0]
            if k == 'pair':
                cap = 2 * nG + nM
            elif k == 'free':
                cap = nG + nM
            else:
                cap = 2 * nM
            if cap < d:
                return False
        # index-wise flag bound (proved in ../PROOFS.md):  the stab-i points
        # still needing degree can only be served by remaining free-line
        # orbits (4 flags each) and remaining stab-i line orbits (2 each)
        for i in NONTRIV:
            need = sum(4 - deg[p] for p in range(23)
                       if self.c.kind[p][0] == 'pair' and self.c.kind[p][1] == i
                       and deg[p] < 4)
            have = 4 * nG + 2 * sum(1 for k in range(si, len(self.slots))
                                    if self.slots[k][0] in ('M', 'L1')
                                    and self.slots[k][1] == i)
            if need > have:
                return False
        return True

    # -------- driver ---------------------------------------------------
    def run(self):
        state = {'adj': [0] * 23, 'deg': [0] * 23, 'lines': []}
        self._descend(0, state, {})
        return self.types

    def _descend(self, si, state, prev_by_type):
        if self.truncated:
            return
        self.nodes += 1
        if self.deadline and (self.nodes & 511) == 0 and time.monotonic() > self.deadline:
            self.truncated = True
            return
        if si == len(self.slots):
            self._leaf(state)
            return
        kind, stab = self.slots[si]
        key = (kind, stab)
        prev = prev_by_type.get(key)
        if si in self.forced:
            cands = [S for S in self.forced[si] if prev is None or S > prev]
        elif kind == 'M':
            cands = [S for S in self.gen_M(stab) if prev is None or S > prev]
        elif kind == 'G':
            cands = self.gen_G(state, prev)
        else:
            raise AssertionError(kind)
        if self.shard is not None and si == self.shard[0]:
            j = self.shard[1]
            cands = cands[j:j + 1]
        for S in cands:
            tok = self.place(S, kind, stab, state)
            if tok is None:
                continue
            if self.feasible(si + 1, state):
                old = prev_by_type.get(key)
                prev_by_type[key] = tuple(S)
                self._descend(si + 1, state, prev_by_type)
                if old is None:
                    del prev_by_type[key]
                else:
                    prev_by_type[key] = old
            else:
                self.rej['feasible'] += 1
            self.unplace(tok, state)
            if self.truncated:
                return

    def _leaf(self, state):
        c = self.c
        if any(d != 4 for d in state['deg']):
            self.rej['final_deg'] += 1
            return
        self.leaves += 1
        if not self.collect:
            return
        if (self.leaves % 50000) == 0:
            print('   .. leaves=%d types=%d (%.0fs)'
                  % (self.leaves, len(self.types), time.monotonic() - self.t0),
                  flush=True)
        lines = [tuple(sorted(l)) for l in state['lines']]
        key = fastcanon.canon(23, lines)
        if key not in self.types:
            bad = av4.validate_n4(23, [frozenset(l) for l in lines])
            bad += av4.validate_equivariance(23, [frozenset(l) for l in lines], c.perms)
            bad += av4.necessary_conditions(23, [frozenset(l) for l in lines], c.perms)
            if bad:
                raise AssertionError('independent enumerator emitted an '
                                     'invalid/fence-violating structure: %s' % bad)
            self.types[key] = lines


def run_cell(b2, b3, bs2, bs3, collect=True, cap=None, force=False, shard=None):
    cell = Cell(b2, b3, bs2, bs3)
    why = admissible(cell)
    t0 = time.monotonic()
    if why and not force:
        return {'cell': cell.name, 'status': 'EMPTY_BY_PROOF', 'reasons': why,
                'types': 0, 'leaves': 0, 'nodes': 0, 'seconds': 0.0}, {}
    e = Enum(cell, collect=collect,
             deadline=(time.monotonic() + cap) if cap else None, shard=shard)
    types = e.run()
    return {
        'cell': cell.name,
        'shard': shard,
        'status': 'TRUNCATED' if e.truncated else 'COMPLETE',
        'cell_admissibility_reasons': why,
        'types': len(types), 'leaves': e.leaves, 'nodes': e.nodes,
        'rejections': dict(e.rej),
        'seconds': round(time.monotonic() - t0, 2),
    }, types


def all_subcells():
    out = []
    for b in (1, 3, 5):
        for bs in (1, 3, 5):
            if 16 - 2 * b - 2 * bs < 0:
                continue
            for b2 in range(b + 1):
                for bs2 in range(bs + 1):
                    k = (b2, b - b2, bs2, bs - bs2)
                    if (k[1], k[0], k[3], k[2]) < k:
                        continue
                    out.append(k)
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cell', help='b2,b3,bs2,bs3')
    ap.add_argument('--all', action='store_true')
    ap.add_argument('--count-only', action='store_true')
    ap.add_argument('--force', action='store_true',
                    help='run even cells proved empty (independent control)')
    ap.add_argument('--cap', type=float, default=0)
    ap.add_argument('--out', default=None)
    ap.add_argument('--shard', default=None,
                    help='SLOT:INDEX -- restrict slot SLOT to its INDEX-th '
                         'candidate (a pure scheduling split of the search '
                         'tree; the union over INDEX is the full run)')
    args = ap.parse_args()
    shard = (tuple(int(x) for x in args.shard.split(':')) if args.shard else None)
    cells = ([tuple(int(x) for x in args.cell.split(','))] if args.cell
             else all_subcells())
    summ = []
    store = {}
    for k in cells:
        s, types = run_cell(*k, collect=not args.count_only,
                            cap=(args.cap or None), force=args.force,
                            shard=shard)
        print(json.dumps(s), flush=True)
        summ.append(s)
        for key, lines in types.items():
            store.setdefault(key, {'lines': lines, 'cells': []})
            store[key]['cells'].append(s['cell'])
    print('TOTAL distinct types:', len(store))
    if args.out:
        with open(args.out, 'w') as fh:
            json.dump({'summary': summ,
                       'n_distinct_types': len(store),
                       'types': [{'lines': v['lines'], 'cells': v['cells']}
                                 for k, v in sorted(store.items(), key=lambda kv: repr(kv[0]))]},
                      fh)


if __name__ == '__main__':
    main()
