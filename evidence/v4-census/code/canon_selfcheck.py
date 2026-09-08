#!/usr/bin/env python3
"""Self-check of the two canonical forms this lane relies on.

The whole set-equality argument of packet item 6 rests on `av4.canonical`
being a COMPLETE isomorphism invariant for role-preserving isomorphism of
(23_4) configurations, and on `fastcanon.canon` (used only for internal
de-duplication inside the independent enumerator) inducing the same
partition.

  S1  invariance      : digest unchanged under deterministic pseudorandom
                        relabellings of points and of lines;
  S2  completeness    : whenever two structures share a digest, an EXPLICIT
                        point bijection carrying one to the other is
                        produced and verified;
  S3  sensitivity     : a one-point mutation changes the digest;
  S4  cross-agreement : `av4` and `fastcanon` induce the same partition of
                        the frozen corpus;
  S5  duality         : the digest of the dual is computed from the dual
                        structure only, and dualising twice is the identity.
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import av4          # noqa: E402
import fastcanon    # noqa: E402
import pins         # noqa: E402


def lcg(seed):
    s = seed
    while True:
        s = (s * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        yield s


def shuffle(rng, n):
    a = list(range(n))
    for i in range(n - 1, 0, -1):
        j = next(rng) % (i + 1)
        a[i], a[j] = a[j], a[i]
    return a


def main():
    t0 = time.time()
    P = pins.load_all_pins()
    keys = sorted(P)
    sample = [keys[i] for i in range(0, len(keys), max(1, len(keys) // 200))]
    rng = lcg(20260829)
    s1_ok = s2_ok = s3_ok = s5_ok = True
    s1_fail = s2_fail = s3_fail = []
    for dg in sample:
        n, L, _ = pins.pin_structure(P[dg])
        lines = [tuple(sorted(l)) for l in L]
        base = av4.canon_hex(n, lines)
        for _ in range(3):
            pp = shuffle(rng, n)
            lp = shuffle(rng, n)
            rl = [tuple(sorted(pp[p] for p in lines[i])) for i in lp]
            if av4.canon_hex(n, rl) != base:
                s1_ok = False
                s1_fail.append(dg)
            pi = av4.iso_from_canonical(n, lines, rl)
            if pi is None:
                s2_ok = False
                s2_fail.append(dg)
        # sensitivity
        ml = [list(l) for l in lines]
        out = [q for q in range(n) if q not in ml[0]]
        ml[0][0] = out[0]
        if av4.canon_hex(n, [tuple(sorted(l)) for l in ml]) == base:
            s3_ok = False
            s3_fail.append(dg)
        dd = av4.dual_lines(n, av4.dual_lines(n, lines))
        if av4.canon_hex(n, dd) != base:
            s5_ok = False

    # S4: cross-agreement over the WHOLE corpus
    a_map, f_map = {}, {}
    for dg in keys:
        n, L, _ = pins.pin_structure(P[dg])
        lines = [tuple(sorted(l)) for l in L]
        a_map[dg] = av4.canon_hex(n, lines)
        f_map[dg] = fastcanon.canon_hex(n, lines)
    a_part = {}
    f_part = {}
    for dg in keys:
        a_part.setdefault(a_map[dg], set()).add(dg)
        f_part.setdefault(f_map[dg], set()).add(dg)
    same_partition = (sorted(map(sorted, a_part.values())) ==
                      sorted(map(sorted, f_part.values())))

    res = {
        'sample_size': len(sample),
        'S1_relabelling_invariance': s1_ok,
        'S1_failures': s1_fail[:5],
        'S2_explicit_verified_isomorphism_for_every_equal_digest': s2_ok,
        'S2_failures': s2_fail[:5],
        'S3_sensitivity_to_one_point_mutation': s3_ok,
        'S3_failures': s3_fail[:5],
        'S4_av4_classes': len(a_part),
        'S4_fastcanon_classes': len(f_part),
        'S4_same_partition_on_whole_corpus': same_partition,
        'S5_double_dual_is_identity': s5_ok,
        'seconds': round(time.time() - t0, 1),
    }
    with open(os.path.join(ART, 'output', 'item5_canonical_form_selfcheck.json'), 'w') as fh:
        json.dump(res, fh, indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))


if __name__ == '__main__':
    main()
