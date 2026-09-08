#!/usr/bin/env python3
"""Resolve the n = 19 control's apparent 9-versus-6 gap.

`small_control19.py` compared the unnormalised brute force against the
normalised enumerator run on ONE cell, `(b2,b3;b*2,b*3) = (0,1;0,1)`.  The
brute force, however, fixes only the POINT orbit inventory: it enumerates
every V4-invariant (19_4) linear space on that labelled point set, so its
output also contains structures whose LINE inventory is the other cell
admissible at n = 19, `(0,1;1,0)`.  A single-cell comparison must
therefore under-count, and the honest comparison is against the union over
the admissible line inventories.

This script records, for every fence-valid type the brute force finds, its
recomputed line inventory, and compares the brute-force set against that
union.  A residual gap here WOULD be a failure of Proposition N-A; the
absence of one is the control that Proposition N-A needed.
"""

import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import av4              # noqa: E402
import fastcanon        # noqa: E402
import small_control as sc          # noqa: E402
import small_control19 as s19       # noqa: E402


def main():
    n = 19
    sysm = sc.Sys(n, [1, 1, 3], 3)

    cells = [(0, 1), (1, 0)]        # admissible (b*_2, b*_3) at this profile
    norm = {}
    for bs2, bs3 in cells:
        na = sc.normalised(sysm, 0, 1, bs2, bs3)
        norm[(bs2, bs3)] = {fastcanon.canon(n, list(l)) for l in na}
        print('normalised bs=(%d,%d): labelled %d types %d'
              % (bs2, bs3, len(na), len(norm[(bs2, bs3)])), flush=True)
    union = set().union(*norm.values())

    t0 = time.time()
    bf, trunc = s19.brute_force_cover(sysm, time.monotonic() + 9000)
    print('brute force %d labelled, truncated=%s (%.0fs)'
          % (len(bf), trunc, time.time() - t0), flush=True)

    fv = {}
    seen_inv = Counter()
    for lines in bf:
        L = [frozenset(l) for l in lines]
        if av4.necessary_conditions(n, L, sysm.perms):
            continue
        k = fastcanon.canon(n, list(lines))
        f, b, a, fs, bs, asx = av4.inventory(n, L, sysm.perms)
        fv.setdefault(k, set()).add((tuple(b), a, tuple(bs), asx))
        seen_inv[(tuple(b), a, tuple(bs), asx)] += 1

    res = {
        'n': n, 'point_profile': sysm.pair_idx, 'a': sysm.a,
        'brute_force_truncated': trunc,
        'brute_force_labelled': len(bf),
        'brute_force_fence_valid_types': len(fv),
        'line_inventories_seen_in_brute_force':
            {str(k): v for k, v in sorted(seen_inv.items())},
        'normalised_per_cell': {str(k): len(v) for k, v in sorted(norm.items())},
        'normalised_union': len(union),
        'SET_EQUALITY_bruteforce_vs_union_over_admissible_line_inventories':
            set(fv) == union,
        'n_missing_from_normalised_union': len(set(fv) - union),
        'n_extra_in_normalised_union': len(union - set(fv)),
        'inventories_of_any_missing_type':
            [sorted(map(str, fv[k])) for k in sorted(set(fv) - union)],
        'seconds': round(time.time() - t0, 1),
    }
    with open(os.path.join(ART, 'output',
                           'item5_small_control_n19_resolved.json'), 'w') as fh:
        json.dump(res, fh, indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))


if __name__ == '__main__':
    main()
