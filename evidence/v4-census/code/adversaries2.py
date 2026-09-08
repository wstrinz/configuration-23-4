#!/usr/bin/env python3
"""Adversary battery, part 2: SENSITIVITY of the instrument.

Part 1 (`adversaries.py`, A2) showed that collapsing the free-coset
("twist") choice in `gen_pairline` at every stab index costs the pinned
generator NOTHING on all six load-bearing cells: the orderly rule absorbs
those candidates.  That is a statement about redundancy, and on its own it
would be equally consistent with "the instrument is blind".

This file therefore plants defects that a correct instrument MUST see, and
measures the loss:

  B1  a NON-necessary prune in `gen_freeline`: forbid a free-line
      representative from carrying two 2-orbit points of different
      stabiliser indices.  (That combination is legal -- it occurs in the
      accepted Cuntz (22_4) -- so this is a genuine premature prune.)
  B2  drop the free-orbit PAIR choice in `gen_pairline`: force o2 = o1+1.
  B3  drop one of the two forced L1 candidates.
  B4  weaken the orderly rule into an over-eager one: reject a candidate
      whenever ANY Gamma-image is <= it (rather than <), which discards
      the candidate that is equal to its own image.

Each is applied to the pinned generator in a scratch copy; the reported
`loss` must be > 0 for B1-B3 (they remove reachable structures), which is
what certifies that the count comparison used throughout this audit is
sensitive.
"""

import importlib.util
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(ART))
sys.path.insert(0, HERE)
import pins   # noqa: E402

PATCHES = {
    'B0_pinned': [],
    'B1_freeline_forbid_mixed_index_pairs': [(
        "                elif k == 'pair':\n"
        "                    if i in used_pairstab:\n"
        "                        continue",
        "                elif k == 'pair':\n"
        "                    if i in used_pairstab or used_pairstab:\n"
        "                        continue")],
    'B2_pairline_drop_orbit_pair_choice': [(
        "            for o2 in range(o1 + 1, a):",
        "            for o2 in range(o1 + 1, min(o1 + 2, a)):")],
    'B3_drop_second_L1_candidate': [(
        "        if a >= 2:\n            l1b.append((0, 3, F0 + 4, F0 + 5))",
        "        if False:\n            l1b.append((0, 3, F0 + 4, F0 + 5))")],
    'B4_overeager_orderly_rule': [(
        "                if t < St:\n                    return False",
        "                if t <= St and gm != tuple(range(ps.n)):\n"
        "                    return False")],
}


def load(name, patches):
    src = subprocess.run(
        ['git', '-C', REPO, 'cat-file', '-p',
         '%s:artifacts/v4-cell-census-v1/code/v4census.py' % pins.SIDECAR],
        capture_output=True, check=True).stdout.decode()
    for old, new in patches:
        assert old in src, 'patch anchor not found: %r' % old[:60]
        src = src.replace(old, new, 1)
    d = os.path.join(ART, '_scratch_pinned', 'code')
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, '_adv2_%s.py' % name)
    with open(path, 'w') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location('adv2_' + name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules['adv2_' + name] = m
    spec.loader.exec_module(m)
    m.REPO = REPO
    return m


def main():
    cells = [(0, 1, 0, 1), (0, 1, 1, 2)]
    cap = 900.0
    base = {}
    rows = []
    for name, patches in PATCHES.items():
        try:
            m = load(name, patches)
        except AssertionError as e:
            rows.append({'adversary': name, 'error': str(e)})
            print(json.dumps(rows[-1]), flush=True)
            continue
        for c in cells:
            try:
                s = m.run_cell('n23', c, 'fence', cap, None)
            except Exception as e:
                s = {'types': None, 'labelled_structures': None,
                     'status': 'ERROR:%r' % e}
            key = 'b%d%d-bs%d%d' % c
            if name == 'B0_pinned':
                base[key] = s
            row = {'adversary': name, 'cell': key, 'types': s['types'],
                   'labelled': s.get('labelled_structures'),
                   'status': s['status'],
                   'loss_vs_pinned': (base[key]['types'] - s['types'])
                   if (name != 'B0_pinned' and s['types'] is not None) else 0}
            rows.append(row)
            print(json.dumps(row), flush=True)
    out = {
        'rows': rows,
        'instrument_is_sensitive': all(
            any(r['adversary'] == nm and r.get('loss_vs_pinned', 0) > 0
                for r in rows)
            for nm in ('B1_freeline_forbid_mixed_index_pairs',
                       'B2_pairline_drop_orbit_pair_choice',
                       'B3_drop_second_L1_candidate')),
    }
    with open(os.path.join(ART, 'output', 'item5_adversaries_sensitivity.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=str)
    print(json.dumps(out, indent=1, default=str))


if __name__ == '__main__':
    main()
