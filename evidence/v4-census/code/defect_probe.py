#!/usr/bin/env python3
"""ADVERSARY / DEFECT PROBE against the pinned sidecar generator.

Finding D1: in `v4census.Search.gen_pairline`, the coset selector

    cos = lambda o, h: (ps.freept(o, min(h, h ^ i)), ps.freept(o, max(h, h ^ i)))

is enumerated over `h in (0, 1)`.  For stab index i = 1 this is a
COLLAPSE: h ^ 1 swaps 0 and 1, so cos(o,0) == cos(o,1), and the
complementary <s_1>-coset {2,3} of that free orbit is never generated.
For i = 2, 3 the two calls do give the two distinct cosets.

This probe (a) exhibits the collapse, (b) instruments the pinned code to
prove that the load-bearing n=23 FENCE census never reaches the defective
branch, and (c) re-runs every CONTROL that does reach it, with and without
a one-line repair, and reports the count difference.

The sidecar module is loaded from a scratch copy of the PINNED blob; no
sidecar result is imported as authority anywhere in this lane.
"""

import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(ART))
SCRATCH = os.path.join(ART, '_scratch_pinned', 'code')
sys.path.insert(0, SCRATCH)

SIDECAR = '858589eb36b2606460f1cb25966b490d857e0e77'


def load_module(name, patched):
    """Load the pinned v4census under a fresh module name, optionally with
    the one-line coset repair applied."""
    import importlib.util
    src = subprocess.run(
        ['git', '-C', REPO, 'cat-file', '-p',
         '%s:artifacts/v4-cell-census-v1/code/v4census.py' % SIDECAR],
        capture_output=True, check=True).stdout.decode()
    if patched:
        old = "cos = lambda o, h: (ps.freept(o, min(h, h ^ i)), ps.freept(o, max(h, h ^ i)))"
        assert old in src, 'defect line not found -- pinned source changed?'
        new = ("_cs = sorted({tuple(sorted((h, h ^ i))) for h in (0,1,2,3)})\n"
               "        cos = lambda o, h: (ps.freept(o, _cs[h][0]), ps.freept(o, _cs[h][1]))")
        src = src.replace(old, new)
    os.makedirs(SCRATCH, exist_ok=True)
    path = os.path.join(SCRATCH, '_gen_%s.py' % name)
    with open(path, 'w') as fh:
        fh.write(src)
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    m.REPO = REPO         # load_cuntz() needs the real repo root
    return m


def instrument(mod):
    """Record every (mode, cell, stab index) at which gen_pairline is
    actually called."""
    calls = []
    orig = mod.Search.gen_pairline

    def wrapper(self, i, state):
        calls.append((self.mode, getattr(self, 'cellname', '?'), i))
        return orig(self, i, state)
    mod.Search.gen_pairline = wrapper
    return calls


def run(mod, kind, args, mode, cap):
    t0 = time.time()
    s = mod.run_cell(kind, args, mode, cap, None)
    s['wall'] = round(time.time() - t0, 1)
    return s


def main():
    out = {'finding': 'D1 gen_pairline coset collapse at stab index 1'}

    # (a) the collapse itself
    base = load_module('vc_base', False)
    ps = base.PointSys(22, 0, [1, 1, 1], 4)
    demo = {}
    for i in (1, 2, 3):
        cos = (lambda o, h, i=i: (ps.freept(o, min(h, h ^ i)),
                                  ps.freept(o, max(h, h ^ i))))
        demo['i=%d' % i] = {'cos(o0,h0)': cos(0, 0), 'cos(o0,h1)': cos(0, 1),
                            'distinct': cos(0, 0) != cos(0, 1),
                            'true_cosets': sorted({tuple(sorted((h, h ^ i)))
                                                   for h in range(4)})}
    out['a_collapse_demo'] = demo

    # (b) instrument the load-bearing n=23 fence cells
    calls = instrument(base)
    fence_calls = {}
    for cell in [(0, 1, 0, 1), (0, 1, 1, 0), (0, 1, 1, 2), (0, 1, 2, 1),
                 (1, 2, 0, 1), (1, 2, 1, 0)]:
        calls.clear()
        run(base, 'n23', cell, 'fence', 25.0)
        fence_calls['b%d%d-bs%d%d' % cell] = sorted({c[2] for c in calls})
    out['b_stab_indices_reaching_gen_pairline_in_n23_fence'] = fence_calls
    out['b_verdict'] = ('n=23 fence mode never calls gen_pairline with i=1; '
                        'the 5,299-pin census is NOT affected by D1'
                        if all(1 not in v for v in fence_calls.values())
                        else 'AFFECTED')

    # (c) controls that DO reach the defective branch
    pat = load_module('vc_patched', True)
    controls = []

    def cmp_control(label, kind, args, mode, cap):
        a = run(base, kind, args, mode, cap)
        b = run(pat, kind, args, mode, cap)
        controls.append({
            'control': label, 'mode': mode,
            'pinned_types': a['types'], 'repaired_types': b['types'],
            'pinned_status': a['status'], 'repaired_status': b['status'],
            'pinned_labelled': a['labelled_structures'],
            'repaired_labelled': b['labelled_structures'],
            'delta': b['types'] - a['types'],
            'wall': (a['wall'], b['wall']),
        })
        print(json.dumps(controls[-1]), flush=True)

    # T3a Cuntz completeness control cell (stab-1 pairline is FORCED here)
    cmp_control('n22 b=(1,1,1) b*=(1,0,0) [Cuntz cell]', 'n22',
                ((1, 1, 1), (1, 0, 0)), 'fence', 600.0)
    # the same cell in ABSTRACT mode -- receipt claims abstract == fence == 1392
    cmp_control('n22 b=(1,1,1) b*=(1,0,0)', 'n22',
                ((1, 1, 1), (1, 0, 0)), 'abstract', 900.0)
    # T3b-iii separation control, both modes
    cmp_control('n22 b=(2,1,0) b*=(2,1,0)', 'n22',
                ((2, 1, 0), (2, 1, 0)), 'fence', 900.0)
    cmp_control('n22 b=(2,1,0) b*=(2,1,0)', 'n22',
                ((2, 1, 0), (2, 1, 0)), 'abstract', 900.0)
    out['c_controls'] = controls

    d = os.path.join(ART, 'output')
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'item5_defect_probe_D1.json'), 'w') as fh:
        json.dump(out, fh, indent=1, default=str)
    print(json.dumps(out, indent=1, default=str))


if __name__ == '__main__':
    main()
