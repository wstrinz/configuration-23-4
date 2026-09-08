#!/usr/bin/env python3
"""Packet item 6 -- exact set correspondence between this lane's
independent enumeration and the frozen 5,299-pin corpus.

Three joins are performed, in increasing strength:

  J1  per-cell type counts   vs `output/summary.json` of the pinned census;
  J2  BARE type sets, both sides canonicalised with THIS lane's `av4`
      canonical form (the primary completeness statement);
  J3  COHERENT action classes, both sides canonicalised with the
      current-main accepted `coherent_ir.coherent_canonical_form`
      (the packet's "through current-main coherent canonical forms").

Only four of the six nonempty cells are enumerated directly; the other two
are obtained by point-line duality, which maps the type set of the cell
(b2,b3;b*2,b*3) bijectively onto that of (b*2,b*3;b2,b3).  The two
self-paired cells give a duality-closure consistency check for free.
"""

import json
import os
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(ART))
sys.path.insert(0, HERE)
import av4          # noqa: E402
import pins         # noqa: E402

CANON_DIR = os.path.join(
    REPO, 'artifacts', 'v4-coherent-canonical-form-pilot-v1', 'canonicalizer')
sys.path.insert(0, CANON_DIR)

CELLS = {'b01-bs01': (0, 1, 0, 1), 'b01-bs10': (0, 1, 1, 0),
         'b01-bs12': (0, 1, 1, 2), 'b01-bs21': (0, 1, 2, 1)}
DUAL_OF = {'b01-bs12': 'b12-bs01', 'b01-bs21': 'b12-bs10',
           'b01-bs01': 'b01-bs01', 'b01-bs10': 'b01-bs10'}


def cell_perms(b2, b3, bs2, bs3):
    import indep_enum as ie
    return ie.Cell(b2, b3, bs2, bs3).perms


def dualize(n, lines, perms):
    dlines = [tuple(sorted(i for i, l in enumerate(lines) if p in l))
              for p in range(n)]
    dperms = tuple(av4.induced_line_perm([frozenset(l) for l in lines], perms, g)
                   for g in av4.V4)
    return dlines, dperms


def build_struct(n, lines, perms):
    """current-main action-struct convention (r = s1, s = s2)."""
    L = [frozenset(l) for l in lines]
    r_l = av4.induced_line_perm(L, perms, 1)
    s_l = av4.induced_line_perm(L, perms, 2)
    inc = [[0] * n for _ in range(n)]
    for li, l in enumerate(lines):
        for p in l:
            inc[p][li] = 1
    return {'n_points': n, 'n_lines': n, 'incidence': inc,
            'r_pts': list(perms[1]), 's_pts': list(perms[2]),
            'r_lns': list(r_l), 's_lns': list(s_l)}


def main():
    t0 = time.time()
    assert sys.flags.optimize == 0, 'assertions must be enabled'
    import coherent_ir

    indep = os.path.join(ART, 'output', 'indep')
    have = {c: os.path.join(indep, c + '.json') for c in CELLS}
    missing = [c for c, p in have.items() if not os.path.exists(p)]
    if missing:
        raise SystemExit('independent enumeration incomplete: %s' % missing)

    # ---------------- load the independent enumeration -----------------
    per_cell = {}
    my_bare = {}                    # av4 digest -> (cell, lines, perms)
    my_coh = {}                     # coherent hex -> (cell, av4 digest)
    my_cell_sets = {}               # cell -> set of av4 digests
    for c, path in sorted(have.items()):
        with open(path) as fh:
            d = json.load(fh)
        assert d['summary'][0]['status'] == 'COMPLETE', (c, d['summary'][0])
        perms = cell_perms(*CELLS[c])
        keys = set()
        for t in d['types']:
            lines = [tuple(sorted(l)) for l in t['lines']]
            dg = av4.canon_hex(23, lines)
            keys.add(dg)
            my_bare.setdefault(dg, (c, lines, perms))
            ch = coherent_ir.coherent_digest_hex(build_struct(23, lines, perms))
            my_coh.setdefault(ch, set()).add((c, dg))
        per_cell[c] = {'types': len(keys), 'declared': d['n_distinct_types'],
                       'summary': d['summary'][0]}
        # the dual cell
        dc = DUAL_OF[c]
        dkeys = set()
        for t in d['types']:
            lines = [tuple(sorted(l)) for l in t['lines']]
            dl, dp = dualize(23, lines, perms)
            dg = av4.canon_hex(23, dl)
            dkeys.add(dg)
            my_bare.setdefault(dg, (dc, dl, dp))
            ch = coherent_ir.coherent_digest_hex(build_struct(23, dl, dp))
            my_coh.setdefault(ch, set()).add((dc, dg))
        per_cell[dc] = per_cell.get(dc, {})
        per_cell[dc]['types_via_duality'] = len(dkeys)
        per_cell[c]['dual_closure_within_cell'] = (dkeys == keys) if dc == c else None
        my_cell_sets[c] = keys
        my_cell_sets.setdefault(dc, set()).update(dkeys)
        print('%s: %d types (dual -> %s: %d)' % (c, len(keys), dc, len(dkeys)),
              flush=True)

    # ---------------- corpus side --------------------------------------
    P = pins.load_all_pins()
    with open(os.path.join(ART, 'output', 'independent_bare_digests.json')) as fh:
        corp = json.load(fh)['sidecar_digest_to_av4_digest']
    corpus_bare = set(corp.values())
    corpus_coh = {}
    for dg, d in sorted(P.items()):
        n, lines, perms = pins.pin_structure(d)
        ch = coherent_ir.coherent_digest_hex(
            build_struct(n, [tuple(sorted(l)) for l in lines], perms))
        corpus_coh.setdefault(ch, set()).add(corp[dg])

    summ = pins.read_json('output/summary.json')
    declared = {c['cell'].replace('n23-fence-', ''): c['types']
                for c in summ['cells'] if c['types']}

    # per-cell type SETS on the corpus side (a pin belongs to its own cell
    # and to every cell listed in `also_found_in`)
    corp_cell_sets = {}
    for dg, d in P.items():
        for cl in [d['cell']] + (d.get('also_found_in') or []):
            corp_cell_sets.setdefault(cl.replace('n23-fence-', ''), set()).add(corp[dg])

    j1 = {}
    for c in sorted(set(list(declared) + list(per_cell))):
        mine = per_cell.get(c, {}).get('types')
        if mine is None:
            mine = per_cell.get(c, {}).get('types_via_duality')
        j1[c] = {'sidecar_types': declared.get(c), 'independent_types': mine,
                 'agree': declared.get(c) == mine,
                 'corpus_cell_set_size': len(corp_cell_sets.get(c, ())),
                 'SET_EQUAL': my_cell_sets.get(c, set()) == corp_cell_sets.get(c, set()),
                 'n_missing': len(corp_cell_sets.get(c, set()) - my_cell_sets.get(c, set())),
                 'n_extra': len(my_cell_sets.get(c, set()) - corp_cell_sets.get(c, set()))}

    res = {
        'J1_per_cell': j1,
        'J1_all_agree': all(v['agree'] for v in j1.values()),
        'J1_all_cell_sets_equal': all(v['SET_EQUAL'] for v in j1.values()),
        'J2_independent_bare_types': len(my_bare),
        'J2_corpus_bare_types': len(corpus_bare),
        'J2_missing_from_independent': sorted(corpus_bare - set(my_bare))[:10],
        'J2_extra_in_independent': sorted(set(my_bare) - corpus_bare)[:10],
        'J2_n_missing': len(corpus_bare - set(my_bare)),
        'J2_n_extra': len(set(my_bare) - corpus_bare),
        'J2_EXACT_SET_EQUALITY': set(my_bare) == corpus_bare,
        'J3_independent_coherent_classes': len(my_coh),
        'J3_corpus_coherent_classes': len(corpus_coh),
        'J3_corpus_subset_of_independent': set(corpus_coh) <= set(my_coh),
        'J3_n_coherent_only_in_independent': len(set(my_coh) - set(corpus_coh)),
        'J3_note': ('the corpus stores exactly one V4 action per bare type; '
                    'a bare type occurring in k of the six sub-cells carries '
                    'k pairwise coherently-inequivalent fence-valid actions, '
                    'so the independent coherent-class count is larger by '
                    'construction and this is NOT a discrepancy'),
        'elapsed_seconds': round(time.time() - t0, 1),
    }
    with open(os.path.join(ART, 'output', 'item6_join.json'), 'w') as fh:
        json.dump(res, fh, indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))


if __name__ == '__main__':
    main()
