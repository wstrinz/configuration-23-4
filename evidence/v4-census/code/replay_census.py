#!/usr/bin/env python3
"""Packet item 4 -- reconcile ALL 54 nominal cells, empty ones included.

Replays the PINNED generator over all 54 nominal sub-cells in fence mode
(the production run itself, which the accepted recanonicalization lane did
NOT re-run: it recanonicalised stored output), and reconciles

  * per-cell COMPLETE/TRUNCATED status and type counts,
  * the 48 empty cells -- against this lane's Theorem C (six-cell), which
    proves them empty,
  * the union of digests against the frozen 5,299-pin corpus,
  * the 72 cross-cell coincidences,
  * and, with `--nogamma CELL`, the same cell with the sidecar's orderly
    rule DISABLED (a premature-prune control on a cell the sidecar's own
    receipt did not test).

The sidecar module is loaded from the pinned blob into a scratch copy; its
outputs are used here as OBJECTS UNDER TEST, never as authority.
"""

import argparse
import importlib.util
import json
import os
import subprocess
import sys
import time
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(ART))
sys.path.insert(0, HERE)
import av4          # noqa: E402
import pins         # noqa: E402
import theory_checks as tc   # noqa: E402


def load_sidecar(name='vc_replay'):
    src = subprocess.run(
        ['git', '-C', REPO, 'cat-file', '-p',
         '%s:artifacts/v4-cell-census-v1/code/v4census.py' % pins.SIDECAR],
        capture_output=True, check=True).stdout.decode()
    d = os.path.join(ART, '_scratch_pinned', 'code')
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, '_%s.py' % name)
    with open(path, 'w') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    m.REPO = REPO
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--nogamma', default=None, help='b2,b3,bs2,bs3')
    ap.add_argument('--cap', type=float, default=1800.0)
    args = ap.parse_args()
    t0 = time.time()
    vc = load_sidecar()

    if args.nogamma:
        os.environ['V4_NOGAMMA'] = '1'
        cell = tuple(int(x) for x in args.nogamma.split(','))
        ps, slots, meta = vc.cell23(*cell, mode='fence')
        se = vc.Search(ps, slots, 'fence', time.monotonic() + args.cap)
        assert se.gamma0 is None, 'V4_NOGAMMA did not take effect'
        res = se.run('n23-fence-b%d%d-bs%d%d' % cell, meta)
        s = {'status': 'TRUNCATED' if se.truncated else 'COMPLETE'}
        got = set(res)
        P = pins.load_all_pins()
        want = {dg for dg, d in P.items()
                if d['cell'] == 'n23-fence-b%d%d-bs%d%d' % cell
                or ('n23-fence-b%d%d-bs%d%d' % cell) in (d.get('also_found_in') or [])}
        out = {'mode': 'V4_NOGAMMA=1 (orderly rule DISABLED)',
               'cell': 'b%d%d-bs%d%d' % cell,
               'status': s['status'], 'nodes': se.nodes,
               'labelled_structures': se.placed_final,
               'types_unpruned': len(got),
               'types_pinned_for_this_cell': len(want),
               'digest_sets_equal': got == want,
               'only_unpruned': sorted(got - want)[:5],
               'only_pinned': sorted(want - got)[:5],
               'seconds': round(time.time() - t0, 1)}
        fn = 'item5_nogamma_%s.json' % out['cell']
        with open(os.path.join(ART, 'output', fn), 'w') as fh:
            json.dump(out, fh, indent=1, default=str)
        print(json.dumps(out, indent=1, default=str))
        return

    # ---- full 54-cell replay
    cells = vc.subcells23()
    assert len(cells) == 54
    surv, dead = tc.six_cell_theorem()
    proved_nonempty = {s[0] for s in surv}
    rows = []
    merged = {}
    for c in cells:
        ps, slots, meta = vc.cell23(*c, mode='fence')
        se = vc.Search(ps, slots, 'fence', time.monotonic() + args.cap)
        name = 'n23-fence-b%d%d-bs%d%d' % c
        res = se.run(name, meta)
        rows.append({'cell': name, 'types': len(res), 'nodes': se.nodes,
                     'labelled': se.placed_final,
                     'status': 'TRUNCATED' if se.truncated else 'COMPLETE',
                     'gamma_enabled': se.gamma0 is not None,
                     'gamma_order': (len(se.gamma0) if se.gamma0 else None),
                     'proved_nonempty_by_theoremC': name in proved_nonempty})
        for dg, r in res.items():
            merged.setdefault(dg, []).append(name)
        print(json.dumps(rows[-1]), flush=True)

    P = pins.load_all_pins()
    pinned = set(P)
    got = set(merged)
    per_cell_sum = sum(r['types'] for r in rows)
    coincid = {dg: v for dg, v in merged.items() if len(v) > 1}
    pinned_coincid = {}
    for dg, d in P.items():
        cl = [d['cell']] + (d.get('also_found_in') or [])
        if len(cl) > 1:
            pinned_coincid[dg] = sorted(cl)

    out = {
        'n_cells_replayed': len(rows),
        'all_complete': all(r['status'] == 'COMPLETE' for r in rows),
        'cells_with_gamma_pruning_disabled_by_cap':
            [r['cell'] for r in rows if not r['gamma_enabled']],
        'nonempty_cells_found': sorted(r['cell'] for r in rows if r['types']),
        'nonempty_cells_proved_by_theoremC': sorted(proved_nonempty),
        'empty_cells_agree_with_theoremC':
            {r['cell'] for r in rows if r['types']} == proved_nonempty,
        'per_cell_types': {r['cell']: r['types'] for r in rows if r['types']},
        'per_cell_type_sum': per_cell_sum,
        'distinct_digests': len(got),
        'corpus_digests': len(pinned),
        'REPLAY_DIGEST_SET_EQUALS_CORPUS': got == pinned,
        'n_only_in_replay': len(got - pinned),
        'n_only_in_corpus': len(pinned - got),
        'cross_cell_coincidences_replay': len(coincid),
        'cross_cell_coincidences_pinned': len(pinned_coincid),
        'coincidence_cellsets_match':
            {dg: sorted(v) for dg, v in coincid.items()} == pinned_coincid,
        'rows': rows,
        'seconds': round(time.time() - t0, 1),
    }
    with open(os.path.join(ART, 'output', 'item4_replay_all_54_cells.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=str)
    print(json.dumps({k: v for k, v in out.items() if k != 'rows'},
                     indent=1, default=str))


if __name__ == '__main__':
    main()
