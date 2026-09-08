#!/usr/bin/env python3
"""Cheap re-check of this lane's headline claims from the COMMITTED compact
indices alone -- no re-enumeration, no sidecar code.

Re-derives, from `output/indep_cell_digests.json` (this lane's independent
enumeration, one canonical digest per type per cell) and
`output/independent_bare_digests.json` (this lane's canonical digest of
every pin of the frozen corpus):

  * per-cell type SET equality, all six cells;
  * global bare-type SET equality (5,299 = 5,299);
  * the 5371 = 5299 + 72 cell-membership reconciliation;
  * the six-cell theorem's cell list;
and re-runs the corpus-side canonical digests on a spot sample so that the
committed index cannot be trusted blindly.
"""

import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import av4          # noqa: E402
import pins         # noqa: E402
import theory_checks as tc   # noqa: E402

OUT = os.path.join(ART, 'output')


def main():
    ind = json.load(open(os.path.join(OUT, 'indep_cell_digests.json')))['cells']
    corpmap = json.load(open(os.path.join(OUT, 'independent_bare_digests.json'))
                        )['sidecar_digest_to_av4_digest']
    P = pins.load_all_pins()

    # spot-check the committed corpus index against a fresh computation
    sample = sorted(P)[::300]
    spot_ok = True
    for dg in sample:
        n, L, _ = pins.pin_structure(P[dg])
        if av4.canon_hex(n, [tuple(sorted(l)) for l in L]) != corpmap[dg]:
            spot_ok = False

    corp_cell = {}
    for dg, d in P.items():
        for cl in [d['cell']] + (d.get('also_found_in') or []):
            corp_cell.setdefault(cl.replace('n23-fence-', ''), set()).add(corpmap[dg])

    per_cell = {}
    for c in sorted(set(list(ind) + list(corp_cell))):
        a, b = set(ind.get(c, [])), corp_cell.get(c, set())
        per_cell[c] = {'independent': len(a), 'corpus': len(b),
                       'set_equal': a == b,
                       'missing': len(b - a), 'extra': len(a - b)}

    union_ind = set().union(*[set(v) for v in ind.values()])
    union_cor = set(corpmap.values())
    memberships = sum(len(v) for v in corp_cell.values())
    surv, dead = tc.six_cell_theorem()

    res = {
        'corpus_index_spot_check_ok': spot_ok,
        'spot_sample': len(sample),
        'per_cell': per_cell,
        'all_cell_sets_equal': all(v['set_equal'] for v in per_cell.values()),
        'union_independent': len(union_ind),
        'union_corpus': len(union_cor),
        'GLOBAL_SET_EQUALITY': union_ind == union_cor,
        'sum_of_cell_memberships': memberships,
        'distinct_types': len(union_cor),
        'excess_memberships': memberships - len(union_cor),
        'reconciliation_5371_equals_5299_plus_72':
            memberships == 5371 and len(union_cor) == 5299,
        'six_cell_theorem_cells': [s[0].replace('n23-fence-', '') for s in surv],
        'six_cell_theorem_matches_nonempty_cells':
            sorted(s[0].replace('n23-fence-', '') for s in surv) ==
            sorted(c for c, v in per_cell.items() if v['corpus']),
        'n_cells_proved_empty': len(dead),
    }
    with open(os.path.join(OUT, 'verify_from_receipts.json'), 'w') as fh:
        json.dump(res, fh, indent=1, default=str)
    print(json.dumps(res, indent=1, default=str))


if __name__ == '__main__':
    main()
