#!/usr/bin/env python3
"""Exhaustive bounded control at n = 19, with an exact-cover search rule.

Same contract as `small_control.py` but the unnormalised brute force uses
the standard exact-cover branching instead of "orbits in increasing
representative order":

  at each node take the SMALLEST point whose degree is still < 4; every
  completion must contain at least one line orbit through that point, so
  branch over all still-allowed orbits through it, and exclude each
  branch's orbit from the later branches.

That rule is exhaustive and duplicate-free (a standard argument: solutions
are partitioned by which of the ordered candidate orbits through the
forced point is the first one they use), and it is dramatically faster
than rep-order enumeration because it never explores partial structures
that leave an early point uncoverable.

No normalisation, no frame, no fence is assumed in the brute force.
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
import small_control as sc   # noqa: E402


def brute_force_cover(sysm, deadline=None):
    n = sysm.n
    orbs = sc.all_orbits(sysm)
    keys = sorted(orbs)
    by_point = defaultdict(list)
    for ki, k in enumerate(keys):
        pts = set()
        for L in orbs[k]:
            pts |= set(L)
        for p in pts:
            by_point[p].append(ki)
    out = []
    deg = [0] * n
    adj = [0] * n
    chosen = []
    nl = [0]
    truncated = [False]

    def can_place(ki):
        add = Counter()
        for L in orbs[keys[ki]]:
            for p in L:
                add[p] += 1
        if any(deg[p] + c > 4 for p, c in add.items()):
            return None
        for L in orbs[keys[ki]]:
            m = 0
            for p in L:
                m |= 1 << p
            for p in L:
                if adj[p] & (m & ~(1 << p)):
                    return None
        # within-orbit consistency: sequential marking
        tmp = list(adj)
        for L in orbs[keys[ki]]:
            m = 0
            for p in L:
                m |= 1 << p
            for p in L:
                if tmp[p] & (m & ~(1 << p)):
                    return None
            for p in L:
                tmp[p] |= m & ~(1 << p)
        return (add, tmp)

    def rec(banned):
        if deadline and time.monotonic() > deadline:
            truncated[0] = True
            return
        if truncated[0]:
            return
        p = next((q for q in range(n) if deg[q] < 4), None)
        if p is None:
            if nl[0] == n:
                out.append(tuple(sorted(L for ki in chosen for L in orbs[keys[ki]])))
            return
        if nl[0] >= n:
            return
        for ki in by_point[p]:
            if ki in banned:
                continue
            r = can_place(ki)
            if r is None:
                banned = banned | {ki}
                continue
            add, newadj = r
            old_adj = list(adj)
            for q, c in add.items():
                deg[q] += c
            adj[:] = newadj
            chosen.append(ki)
            nl[0] += len(orbs[keys[ki]])
            rec(banned)
            nl[0] -= len(orbs[keys[ki]])
            chosen.pop()
            adj[:] = old_adj
            for q, c in add.items():
                deg[q] -= c
            banned = banned | {ki}
            if truncated[0]:
                return
    rec(frozenset())
    return out, truncated[0]


def main():
    t0 = time.time()
    n, b2, b3, bs2, bs3 = 19, 0, 1, 0, 1
    a = (n - 5 - 2 * (b2 + b3)) // 4
    sysm = sc.Sys(n, [1, 1] + [2] * b2 + [3] * b3, a)
    cap = float(sys.argv[1]) if len(sys.argv) > 1 else 7200.0
    bf, trunc = brute_force_cover(sysm, time.monotonic() + cap)
    print('brute force: %d labelled structures, truncated=%s (%.0fs)'
          % (len(bf), trunc, time.time() - t0), flush=True)

    bf_keys = Counter()
    bf_fence = Counter()
    bf_reps = {}
    for lines in bf:
        k = fastcanon.canon(n, list(lines))
        bf_keys[k] += 1
        bf_reps.setdefault(k, lines)
        if not av4.necessary_conditions(n, [frozenset(l) for l in lines], sysm.perms):
            bf_fence[k] += 1
    fenceset = {k for k, v in bf_fence.items() if v > 0}

    na = sc.normalised(sysm, b2, b3, bs2, bs3)
    na_keys = {fastcanon.canon(n, list(l)) for l in na}

    prune_variants = {}
    for pr in (('bad',), ('omin',), ()):
        v = sc.normalised(sysm, b2, b3, bs2, bs3, prunes=pr)
        s = {fastcanon.canon(n, list(l)) for l in v}
        prune_variants['prunes=%s' % (pr,)] = {'labelled': len(v), 'types': len(s),
                                               'same_type_set': s == na_keys}

    G = sysm.gamma()
    mult = {}
    for k, rep in bf_reps.items():
        mult[k] = len({tuple(sorted(tuple(sorted(gm[p] for p in l)) for l in rep))
                       for gm in G})

    res = {
        'profile': {'n': n, 'pair_idx': sysm.pair_idx, 'a': a,
                    'cell': 'n19-b01-bs01'},
        'brute_force_truncated': trunc,
        'brute_force_labelled_structures': len(bf),
        'brute_force_bare_types': len(bf_keys),
        'brute_force_fence_valid_types': len(fenceset),
        'fence_validity_is_type_level':
            all(bf_fence[k] in (0, bf_keys[k]) for k in bf_keys),
        'normalised_labelled_structures': len(na),
        'normalised_bare_types': len(na_keys),
        'gamma_order': len(G),
        'SET_EQUALITY_normalised_vs_bruteforce_fencevalid': na_keys == fenceset,
        'missing_from_normalised': len(fenceset - na_keys),
        'extra_in_normalised': len(na_keys - fenceset),
        'MULTIPLICITY_gamma_orbit_equals_bruteforce_count':
            all(mult[k] == bf_keys[k] for k in bf_keys),
        'A4_premature_prune_variants': prune_variants,
        'abstract_vs_geometric_separation': {
            'types_satisfying_only_the_abstract_axioms': len(bf_keys) - len(fenceset),
            'types_also_fence_valid': len(fenceset)},
        'seconds': round(time.time() - t0, 1),
    }
    with open(os.path.join(os.path.dirname(HERE), 'output',
                           'item5_small_control_n19.json'), 'w') as fh:
        json.dump(res, fh, indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))


if __name__ == '__main__':
    main()
