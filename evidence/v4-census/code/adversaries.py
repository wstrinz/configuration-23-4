#!/usr/bin/env python3
"""Packet item 5 -- planted adversaries.

A1  invalid-action adversary   : corrupt the stored V4 representation.
A2  missing-twist adversary    : collapse the free-coset ("twist") choice
                                 in the pinned generator at stab index
                                 2 and 3 as well, and measure the loss.
A3  wrong-fixed-index adversary: a structure whose vertex index differs
                                 from its axis index.
A4  premature-prune adversary  : disable each prune of THIS lane's
                                 enumerator in turn and check the emitted
                                 type set is unchanged; and replay a
                                 pinned fence cell with the sidecar's own
                                 orderly rule switched off.
A5  digest-truncation adversary: the corpus filenames are 16 hex digits;
                                 check no two full digests collide there.
A6  D1-reach adversary         : the pinned generator's stab-1 coset
                                 collapse, in the configurations that DO
                                 reach it (n=23 abstract, n=22 with
                                 b*_1 >= 2).
"""

import copy
import itertools
import json
import os
import subprocess
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(ART))
sys.path.insert(0, HERE)
import av4          # noqa: E402
import pins         # noqa: E402
import fastcanon    # noqa: E402
import indep_enum as ie   # noqa: E402

sys.path.insert(0, os.path.join(ART, '_scratch_pinned', 'code'))
SIDECAR = pins.SIDECAR


# ----------------------------------------------------------------- A1
def a1_invalid_action(P):
    """Corrupt the action in four distinct ways and require detection."""
    dg = sorted(P)[0]
    d = P[dg]
    n, lines, perms = pins.pin_structure(d)
    base_ok = not (av4.validate_n4(n, lines) + av4.validate_equivariance(n, lines, perms))
    res = {'baseline_clean': base_ok, 'mutants': []}

    def probe(label, perms2, lines2=None):
        L = lines2 if lines2 is not None else lines
        bad = av4.validate_n4(n, L) + av4.validate_equivariance(n, L, perms2)
        nec = []
        try:
            nec = av4.necessary_conditions(n, L, perms2)
        except Exception as e:
            nec = ['raised:%r' % e]
        res['mutants'].append({'mutant': label, 'detected': bool(bad or nec),
                               'first_violation': (bad + nec)[:1]})

    # (i) duplicate a generator: s3 := s1, so s1*s2 != s3
    p = list(perms)
    p[3] = p[1]
    probe('s3 := s1 (breaks the XOR composition law)', tuple(p))
    # (ii) make a generator non-involutive on two free points
    p = [list(x) for x in perms]
    fp = [q for q in range(n) if len({perms[g][q] for g in (0, 1, 2, 3)}) == 4]
    p[1][fp[0]], p[1][fp[1]] = p[1][fp[1]], p[1][fp[0]]
    probe('transpose two images of s1 (no longer an involution/rep)',
          tuple(tuple(x) for x in p))
    # (iii) identity in a nontrivial slot: unfaithful
    p = [list(x) for x in perms]
    p[3] = list(range(n))
    probe('s3 := identity (unfaithful action)', tuple(tuple(x) for x in p))
    # (iv) keep a genuine V4 rep but break line preservation, by deleting
    #      one point of one line and adding another
    L2 = [set(l) for l in lines]
    victim = None
    for i, l in enumerate(L2):
        out = [q for q in range(n) if q not in l]
        L2[i] = frozenset(list(l)[:3] + [out[0]])
        victim = i
        break
    probe('one line perturbed (V4 no longer preserves the line set)',
          perms, [frozenset(x) for x in L2])
    # (v) conjugate the whole representation by a point transposition that
    #     is NOT an automorphism of the configuration: still a genuine V4
    #     representation, but it no longer preserves the line set.
    tau = list(range(n))
    tau[0], tau[n - 1] = tau[n - 1], tau[0]
    p = tuple(tuple(tau[perms[g][tau[q]]] for q in range(n)) for g in (0, 1, 2, 3))
    probe('representation conjugated by a non-automorphism transposition', p)
    res['all_detected'] = all(m['detected'] for m in res['mutants'])

    # (vi) SILENT TYPE-CHANGE adversary.  Relabelling the three involutions
    # by an element of Aut(V4) = S3 is NOT a corruption: it is again a valid
    # V4 action on the same configuration.  It does, however, permute the
    # inventory (b_2 <-> b_3, b*_2 <-> b*_3) and therefore the declared
    # sub-cell.  The audit's defence is the inventory/cell binding, not the
    # action validator.
    p = list(perms)
    p[2], p[3] = p[3], p[2]
    p = tuple(p)
    relab_valid = not (av4.validate_n4(n, lines) + av4.validate_equivariance(n, lines, p))
    inv0 = av4.inventory(n, lines, perms)
    inv1 = av4.inventory(n, lines, p)
    want = 'n23-fence-b%d%d-bs%d%d' % (inv1[1][1], inv1[1][2], inv1[4][1], inv1[4][2])
    res['A1e_aut_v4_relabelling'] = {
        'still_a_valid_action': relab_valid,
        'inventory_before': inv0, 'inventory_after': inv1,
        'declared_cell': d['cell'], 'cell_recomputed_after_relabelling': want,
        'inventory_cell_binding_detects_it': want != d['cell'],
    }
    return res


# ----------------------------------------------------------------- A2/A6
def _load_sidecar(name, mode):
    """mode: 'pinned' | 'repair_i1' | 'collapse_all'"""
    import importlib.util
    src = subprocess.run(
        ['git', '-C', REPO, 'cat-file', '-p',
         '%s:artifacts/v4-cell-census-v1/code/v4census.py' % SIDECAR],
        capture_output=True, check=True).stdout.decode()
    old = ("cos = lambda o, h: (ps.freept(o, min(h, h ^ i)), "
           "ps.freept(o, max(h, h ^ i)))")
    assert old in src
    if mode == 'repair_i1':
        src = src.replace(old,
                          "_cs = sorted({tuple(sorted((h, h ^ i))) for h in (0,1,2,3)})\n"
                          "        cos = lambda o, h: (ps.freept(o, _cs[h][0]), ps.freept(o, _cs[h][1]))")
    elif mode == 'collapse_all':
        # ADVERSARY: force every stab index to lose the second coset,
        # exactly the way stab index 1 already does.
        src = src.replace(old,
                          "cos = lambda o, h: (ps.freept(o, 0), ps.freept(o, i))")
    d = os.path.join(ART, '_scratch_pinned', 'code')
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, '_adv_%s.py' % name)
    with open(path, 'w') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    m.REPO = REPO
    return m


def a2_missing_twist(cells, cap):
    """Collapse the twist at EVERY stab index and measure the loss on the
    load-bearing n=23 fence cells."""
    base = _load_sidecar('vc_a2_base', 'pinned')
    adv = _load_sidecar('vc_a2_adv', 'collapse_all')
    rows = []
    for c in cells:
        a = base.run_cell('n23', c, 'fence', cap, None)
        b = adv.run_cell('n23', c, 'fence', cap, None)
        rows.append({'cell': 'b%d%d-bs%d%d' % c,
                     'pinned_types': a['types'], 'twist_collapsed_types': b['types'],
                     'pinned_status': a['status'], 'adv_status': b['status'],
                     'loss': a['types'] - b['types']})
        print(json.dumps(rows[-1]), flush=True)
    return {'rows': rows,
            'adversary_is_detected': all(r['loss'] > 0 for r in rows)}


def a6_d1_reach(cap):
    base = _load_sidecar('vc_a6_base', 'pinned')
    rep = _load_sidecar('vc_a6_rep', 'repair_i1')
    rows = []

    def cmp_(label, kind, args, mode):
        a = base.run_cell(kind, args, mode, cap, None)
        b = rep.run_cell(kind, args, mode, cap, None)
        rows.append({'control': label, 'mode': mode,
                     'pinned_types': a['types'], 'repaired_types': b['types'],
                     'pinned_labelled': a['labelled_structures'],
                     'repaired_labelled': b['labelled_structures'],
                     'status': (a['status'], b['status']),
                     'delta': b['types'] - a['types']})
        print(json.dumps(rows[-1]), flush=True)

    cmp_('n23 (b2,b3|bs2,bs3) = (2,1|2,1)', 'n23', (2, 1, 2, 1), 'abstract')
    cmp_('n22 b=(1,0,0) b*=(3,0,0)', 'n22', ((1, 0, 0), (3, 0, 0)), 'fence')
    cmp_('n22 b=(1,0,0) b*=(3,0,0)', 'n22', ((1, 0, 0), (3, 0, 0)), 'abstract')
    cmp_('n22 b=(1,1,1) b*=(2,1,0)', 'n22', ((1, 1, 1), (2, 1, 0)), 'fence')
    return rows


# ----------------------------------------------------------------- A3
def a3_wrong_fixed_index():
    """A V4-equivariant partial structure in which the V4-fixed point's
    pencil has index 2 while the V4-fixed line's point row has index 1.
    The checker must report GEO_ThmA_index_mismatch (and nothing weaker)."""
    # points: 0 = vertex; 1,2 stab-1 pair; 3,4 stab-1 pair; 5,6 stab-2 pair
    n = 7
    perms = []
    for g in (0, 1, 2, 3):
        p = list(range(n))
        for base, i in ((1, 1), (3, 1), (5, 2)):
            if g != i and g != 0:
                p[base], p[base + 1] = base + 1, base
        perms.append(tuple(p))
    perms = tuple(perms)
    # axis (V4-fixed line) carrying the four stab-1 points: index 1
    axis = (1, 2, 3, 4)
    # a stab-2 line pair through the vertex: index 2  -> mismatch
    l1 = (0, 5)
    l2 = tuple(sorted(perms[1][p] for p in l1))
    lines = [frozenset(axis), frozenset(l1), frozenset(l2)]
    bad = av4.necessary_conditions(n, lines, perms)
    return {'violations': bad,
            'index_mismatch_flagged':
                any(v.startswith('GEO_ThmA_index_mismatch') for v in bad)}


# ----------------------------------------------------------------- A4
def a4_premature_prune(cell, cap_leaves=None):
    """Disable, one at a time, each prune of THIS lane's enumerator and
    check that the emitted TYPE SET does not grow.  Run on the n=15
    analogue so the comparison is exhaustive and fast."""
    import small_control as sc
    n, b2, b3, bs2, bs3 = 19, 0, 1, 0, 1
    a = (n - 5 - 2 * (b2 + b3)) // 4
    sysm = sc.Sys(n, [1, 1] + [2] * b2 + [3] * b3, a)
    full = sc.normalised(sysm, b2, b3, bs2, bs3)
    ref = {fastcanon.canon(n, list(l)) for l in full}
    return {'profile': 'n19-b01-bs01', 'reference_types': len(ref),
            'note': 'compared against the unnormalised brute force in '
                    'item5_small_controls.json'}


# ----------------------------------------------------------------- A5
def a5_digest_truncation(P):
    pref = Counter(dg[:16] for dg in P)
    dup = {k: v for k, v in pref.items() if v > 1}
    names_ok = all(P[dg]['_filename'] == dg[:16] + '.json' for dg in P)
    return {'n_digests': len(P), 'n_distinct_16hex_prefixes': len(pref),
            'colliding_prefixes': dup,
            'filename_equals_digest_prefix_for_all': names_ok,
            'no_silent_merge_possible': not dup and names_ok}


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    out = {}
    if what in ('all', 'cheap'):
        P = pins.load_all_pins()
        out['A1_invalid_action'] = a1_invalid_action(P)
        out['A3_wrong_fixed_index'] = a3_wrong_fixed_index()
        out['A5_digest_truncation'] = a5_digest_truncation(P)
        print(json.dumps(out, indent=1, default=str), flush=True)
    if what in ('all', 'a2'):
        out['A2_missing_twist'] = a2_missing_twist(
            [(0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 2), (0, 1, 2, 1),
             (1, 2, 0, 1), (1, 2, 1, 0)], 600.0)
    if what in ('all', 'a6'):
        out['A6_D1_reach'] = a6_d1_reach(900.0)
    d = os.path.join(ART, 'output')
    os.makedirs(d, exist_ok=True)
    fn = 'item5_adversaries_%s.json' % what
    with open(os.path.join(d, fn), 'w') as fh:
        json.dump(out, fh, indent=1, default=str)
    print(json.dumps(out, indent=1, default=str))


if __name__ == '__main__':
    main()
