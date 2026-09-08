#!/usr/bin/env python3
"""Packet item 3 (first direction) + item 4 bookkeeping.

INDEPENDENT verification that every emitted object of the frozen 5,299-pin
corpus really does satisfy the declared inventories, the necessary
geometric fences, the Theorem A/B frame, and the free-orbit separation
Lemma D of this lane's own derivation -- plus an independent bare
canonical partition and dual closure.

Nothing here is read from the producer except the raw pin bytes.
"""

import json
import os
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import av4          # noqa: E402
import pins         # noqa: E402

OUT = os.path.join(os.path.dirname(HERE), 'output')


def structural_checks(n, lines, perms):
    """Theorem A/B(1)-(4) + Lemma D, recomputed from (lines, perms)."""
    bad = []
    pstab, lstab, _ = av4.taxonomy(n, lines, perms)
    lsets = list(lines)
    Vp = [p for p in range(n) if pstab[p] == av4.FULL]
    Vl = [k for k in range(len(lsets)) if lstab[k] == av4.FULL]
    if len(Vp) != 1 or len(Vl) != 1:
        return ['ThmA:f=%d,fstar=%d' % (len(Vp), len(Vl))]
    x, K = Vp[0], Vl[0]
    # index m of the frame
    ms = {next(iter(pstab[p] - {0})) for p in lsets[K]}
    if len(ms) != 1:
        return ['ThmA:axis_index=%s' % sorted(ms)]
    m = ms.pop()
    # point / line orbits by stabiliser index
    def orbits_of(elems, stabs, act):
        seen, out = set(), []
        for e in elems:
            if e in seen:
                continue
            o = tuple(sorted({act(g, e) for g in av4.V4}))
            seen.update(o)
            out.append(o)
        return out
    lperm = {g: av4.induced_line_perm(lsets, perms, g) for g in av4.V4}
    Porb = {i: orbits_of([p for p in range(n) if pstab[p] == frozenset({0, i})],
                         pstab, lambda g, p: perms[g][p]) for i in av4.NONTRIV}
    Lorb = {i: orbits_of([k for k in range(len(lsets)) if lstab[k] == frozenset({0, i})],
                         lstab, lambda g, k: lperm[g][k]) for i in av4.NONTRIV}
    Forb = orbits_of([p for p in range(n) if pstab[p] == frozenset({0})],
                     pstab, lambda g, p: perms[g][p])
    Gorb = orbits_of([k for k in range(len(lsets)) if lstab[k] == frozenset({0})],
                     lstab, lambda g, k: lperm[g][k])

    # Theorem A: b_m = bstar_m = 2, and the axis / pencil are exact
    if len(Porb[m]) != 2:
        bad.append('ThmA:b_%d=%d!=2' % (m, len(Porb[m])))
    if len(Lorb[m]) != 2:
        bad.append('ThmA:bstar_%d=%d!=2' % (m, len(Lorb[m])))
    if set(lsets[K]) != {p for o in Porb[m] for p in o}:
        bad.append('ThmA:axis_content')
    thru = {k for k in range(len(lsets)) if x in lsets[k]}
    if thru != {k for o in Lorb[m] for k in o}:
        bad.append('ThmA:vertex_pencil')

    # Theorem B(2): perfect matching between the two P_m and two L_m orbits
    match = defaultdict(list)
    for ti, po in enumerate(Porb[m]):
        for si, lo in enumerate(Lorb[m]):
            hits = sum(1 for p in po for k in lo if p in lsets[k])
            if hits:
                match[ti].append((si, hits))
    if sorted((ti, tuple(v)) for ti, v in match.items()) and \
       (len(match) != 2 or any(len(v) != 1 or v[0][1] != 2 for v in match.values())
            or len({v[0][0] for v in match.values()}) != 2):
        bad.append('ThmB2:matching=%s' % dict(match))

    # Theorem B(3): for i != m, P_i orbits meet NO L_i line
    for i in av4.NONTRIV:
        if i == m:
            continue
        for po in Porb[i]:
            for lo in Lorb[i]:
                if any(p in lsets[k] for p in po for k in lo):
                    bad.append('ThmB3:i=%d_nonempty_matching' % i)

    # Theorem B(2)/(3) class counts with free orbits
    for i in av4.NONTRIV:
        want = 1 if i == m else 2
        for po in Porb[i]:
            nb = [gi for gi, go in enumerate(Gorb)
                  if any(p in lsets[k] for p in po for k in go)]
            if len(nb) != want:
                bad.append('ThmB:P_%d_orbit_free_line_classes=%d(want %d)'
                           % (i, len(nb), want))
        for lo in Lorb[i]:
            nb = [fi for fi, fo in enumerate(Forb)
                  if any(p in lsets[k] for p in fo for k in lo)]
            if len(nb) != want:
                bad.append('ThmB:L_%d_orbit_free_pt_classes=%d(want %d)'
                           % (i, len(nb), want))

    # Lemma D: same-index line orbits have disjoint free-point neighbourhoods;
    # different-index line orbits share at most one.
    Nl = {}
    for i in av4.NONTRIV:
        for si, lo in enumerate(Lorb[i]):
            Nl[(i, si)] = {fi for fi, fo in enumerate(Forb)
                           if any(p in lsets[k] for p in fo for k in lo)}
    for (i, si), A in Nl.items():
        for (j, sj), B in Nl.items():
            if (i, si) >= (j, sj):
                continue
            if i == j and A & B:
                bad.append('LemmaD_a:i=%d orbits %d,%d share %s' % (i, si, sj, sorted(A & B)))
            if i != j and len(A & B) > 1:
                bad.append('LemmaD_b:i=%d,j=%d share %s' % (i, j, sorted(A & B)))
    Np = {}
    for i in av4.NONTRIV:
        for ti, po in enumerate(Porb[i]):
            Np[(i, ti)] = {gi for gi, go in enumerate(Gorb)
                           if any(p in lsets[k] for p in po for k in go)}
    for (i, ti), A in Np.items():
        for (j, tj), B in Np.items():
            if (i, ti) >= (j, tj):
                continue
            if i == j and A & B:
                bad.append('LemmaD_a_dual:i=%d share %s' % (i, sorted(A & B)))
            if i != j and len(A & B) > 1:
                bad.append('LemmaD_b_dual:i=%d,j=%d share %s' % (i, j, sorted(A & B)))
    return bad


def main():
    t0 = time.time()
    pins.verify_pinned()
    blobs = {p: pins.blob_hash(p) for p in
             ['DERIVATION.md', 'RECEIPT.md', 'code/v4census.py',
              'code/run_census.py', 'output/summary.json']}
    summary = pins.read_json('output/summary.json')
    P = pins.load_all_pins()
    print('loaded %d pins in %.1fs' % (len(P), time.time() - t0), flush=True)

    anomalies = defaultdict(list)
    my_canon = {}
    my_dual = {}
    inv_by_digest = {}
    cellcount = Counter()
    also_found = 0
    coincidences = []
    n_checked = 0

    for dg in sorted(P):
        d = P[dg]
        n, lines, perms = pins.pin_structure(d)
        if n != 23:
            anomalies['n_not_23'].append(dg)
            continue
        for tag, res in (('n4', av4.validate_n4(n, lines)),
                         ('equivariance', av4.validate_equivariance(n, lines, perms))):
            if res:
                anomalies[tag].append((dg, res))
        # faithfulness of the INDUCED abstract action (Lemma 4)
        lp = {g: av4.induced_line_perm(lines, perms, g) for g in av4.V4}
        for g in av4.NONTRIV:
            if tuple(perms[g]) == tuple(range(n)) and lp[g] == tuple(range(n)):
                anomalies['induced_action_unfaithful'].append((dg, g))
        try:
            inv = av4.inventory(n, lines, perms)
        except ValueError as e:
            anomalies['inventory_error'].append((dg, repr(e)))
            continue
        inv_by_digest[dg] = inv
        f, b, a, fs, bs, asx = inv
        meta = d['cellmeta']
        if [f, b, a, fs, bs, asx] != [1, meta['b'], meta['a'], 1, meta['bstar'], meta['astar']]:
            anomalies['inventory_mismatch'].append((dg, inv, meta))
        if 1 + 2 * sum(b) + 4 * a != 23 or 1 + 2 * sum(bs) + 4 * asx != 23:
            anomalies['inventory_arith'].append((dg, inv))
        nec = av4.necessary_conditions(n, lines, perms)
        if nec:
            anomalies['necessary_conditions'].append((dg, nec))
        st = structural_checks(n, lines, perms)
        if st:
            anomalies['structure'].append((dg, st))
        ck = av4.canon_hex(n, lines)
        my_canon[dg] = ck
        my_dual[dg] = av4.canon_hex(n, av4.dual_lines(n, lines))
        cellcount[d['cell']] += 1
        if d.get('also_found_in'):
            also_found += 1
            coincidences.append((dg, d['cell'], d['also_found_in']))
        n_checked += 1
        if n_checked % 500 == 0:
            print('  ...%d checked (%.0fs)' % (n_checked, time.time() - t0), flush=True)

    # ---- global bookkeeping
    rev = defaultdict(list)
    for dg, ck in my_canon.items():
        rev[ck].append(dg)
    my_classes = len(rev)
    collisions = {ck: v for ck, v in rev.items() if len(v) > 1}

    # dual closure under MY canonical form
    ck_set = set(my_canon.values())
    self_dual = sum(1 for dg in my_canon if my_dual[dg] == my_canon[dg])
    dual_in = sum(1 for dg in my_canon if my_dual[dg] != my_canon[dg]
                  and my_dual[dg] in ck_set)
    dual_missing = [dg for dg in my_canon
                    if my_dual[dg] != my_canon[dg] and my_dual[dg] not in ck_set]

    # declared-vs-computed cell name
    cellname_bad = []
    for dg in sorted(inv_by_digest):
        f, b, a, fs, bs, asx = inv_by_digest[dg]
        want = 'n23-fence-b%d%d-bs%d%d' % (b[1], b[2], bs[1], bs[2])
        if want != P[dg]['cell']:
            cellname_bad.append((dg, want, P[dg]['cell']))

    # sub-cell profile actually occupied
    profiles = Counter()
    for dg, (f, b, a, fs, bs, asx) in inv_by_digest.items():
        profiles[(tuple(b), tuple(bs))] += 1

    res = {
        'sidecar_commit': pins.SIDECAR,
        'source_blob_hashes': blobs,
        'n_pins': len(P),
        'n_fully_checked': n_checked,
        'anomaly_counts': {k: len(v) for k, v in anomalies.items()},
        'anomalies_sample': {k: v[:5] for k, v in anomalies.items()},
        'independent_bare_classes': my_classes,
        'independent_bare_collisions': {k: v for k, v in list(collisions.items())[:5]},
        'independent_partition_is_bijective_with_stored_digests':
            my_classes == len(P) and not collisions,
        'dual_closure': {
            'self_dual': self_dual,
            'dual_in_census': dual_in,
            'dual_missing': len(dual_missing),
        },
        'declared_cellname_mismatches': cellname_bad[:5],
        'n_declared_cellname_mismatches': len(cellname_bad),
        'cell_counts': dict(sorted(cellcount.items())),
        'occupied_profiles': {str(k): v for k, v in sorted(profiles.items())},
        'n_pins_with_also_found_in': also_found,
        'cross_cell_coincidences_sample': coincidences[:5],
        'summary_json_declared_total': summary['total_types'],
        'summary_json_per_cell_sum': sum(c['types'] for c in summary['cells']),
        'elapsed_seconds': round(time.time() - t0, 1),
    }
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, 'item3a_corpus_soundness.json'), 'w') as fh:
        json.dump(res, fh, indent=1, default=str)
    with open(os.path.join(OUT, 'independent_bare_digests.json'), 'w') as fh:
        json.dump({'sidecar_digest_to_av4_digest': my_canon,
                   'sidecar_digest_to_av4_dual_digest': my_dual}, fh)
    print(json.dumps({k: v for k, v in res.items()
                      if k not in ('anomalies_sample', 'occupied_profiles')},
                     indent=1, default=str))
    print('profiles:', res['occupied_profiles'])


if __name__ == '__main__':
    main()
