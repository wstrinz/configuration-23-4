#!/usr/bin/env python3
"""Pinned-blob reader for the frozen V4 sidecar corpus.

Reads the 5,299 type pins and the census receipts as INERT DATA from the
pinned git objects at the sidecar source commit named in the launch packet.
Never imports sidecar code; never reads the working tree.
"""

import json
import os
import subprocess
import sys

SIDECAR = '858589eb36b2606460f1cb25966b490d857e0e77'
SIDECAR_DIR = 'artifacts/v4-cell-census-v1'

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(ART))


def _git(*args, binary=False):
    r = subprocess.run(['git', '-C', REPO] + list(args),
                       capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode()


def verify_pinned():
    t = _git('cat-file', '-t', SIDECAR).strip()
    assert t == 'commit', 'sidecar commit not reachable: %r' % t
    return SIDECAR


def blob_hash(path):
    return _git('rev-parse', '%s:%s/%s' % (SIDECAR, SIDECAR_DIR, path)).strip()


def read_text(path):
    return _git('cat-file', '-p', '%s:%s/%s' % (SIDECAR, SIDECAR_DIR, path))


def read_json(path):
    return json.loads(read_text(path))


def list_pin_files():
    out = _git('ls-tree', '--name-only', '%s:%s/output/types' % (SIDECAR, SIDECAR_DIR))
    return sorted(x for x in out.split('\n') if x.endswith('.json'))


def load_all_pins():
    """digest -> pin dict, for all pins, via one `git cat-file --batch`."""
    names = list_pin_files()
    spec = '\n'.join('%s:%s/output/types/%s' % (SIDECAR, SIDECAR_DIR, nm)
                     for nm in names) + '\n'
    p = subprocess.Popen(['git', '-C', REPO, 'cat-file', '--batch'],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, _ = p.communicate(spec.encode())
    assert p.returncode == 0
    pins = {}
    pos = 0
    for nm in names:
        nl = out.index(b'\n', pos)
        header = out[pos:nl].decode().split()
        size = int(header[2])
        body = out[nl + 1:nl + 1 + size]
        pos = nl + 1 + size + 1
        d = json.loads(body)
        d['_filename'] = nm
        d['_blob'] = header[0]
        dg = d['digest']
        assert dg not in pins, 'duplicate digest %s' % dg
        pins[dg] = d
    assert pos == len(out), 'batch stream not fully consumed'
    return pins


def pin_structure(d):
    """(n, lines, perms) with lines as frozensets, perms as tuples."""
    n = d['n']
    lines = [frozenset(l) for l in d['lines']]
    perms = tuple(tuple(p) for p in d['perms'])
    return n, lines, perms


if __name__ == '__main__':
    verify_pinned()
    for p in ['DERIVATION.md', 'RECEIPT.md', 'code/v4census.py',
              'code/run_census.py', 'output/summary.json']:
        print(blob_hash(p), p)
    names = list_pin_files()
    print('pin files:', len(names))
