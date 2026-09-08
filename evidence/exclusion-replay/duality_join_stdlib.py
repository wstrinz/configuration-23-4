"""Stdlib replay of the frozen independent audit's action-level duality join.

This deliberately does not invoke the census producer or its NetworkX-backed
canonicalizer.  It verifies the hash-pinned, independently generated per-type
records and checks that primal and dual action digests agree as multisets with
the declared reciprocal cell map.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
CFG = HERE.parents[1]
SOURCE = (CFG / "artifacts" /
          "v4-complete-action-pair-census-independent-audit-v1" /
          "output" / "stage1_per_type")

manifest_raw = (SOURCE / "MANIFEST.json").read_bytes()
manifest = json.loads(manifest_raw)
per_type = {}
for name, pin in manifest["files"].items():
    raw = (SOURCE / name).read_bytes()
    assert len(raw) == pin["bytes"]
    assert hashlib.sha256(raw).hexdigest() == pin["sha256"]
    part = json.loads(raw)
    assert len(part) == pin["n_keys"]
    assert not (set(per_type) & set(part))
    per_type.update(part)
assert len(per_type) == manifest["n_keys"] == 5299

primal = Counter()
dual = Counter()
cellmap = Counter()
for row in per_type.values():
    for action in row["retained"]:
        primal[action["cdigest"]] += 1
        dual[action["dual_cdigest"]] += 1
        cellmap[(action["cell"], action["dual_cell"])] += 1
assert sum(primal.values()) == 5395
assert primal == dual
reciprocal = {
    "n23-fence-b01-bs01": "n23-fence-b01-bs01",
    "n23-fence-b01-bs10": "n23-fence-b01-bs10",
    "n23-fence-b01-bs12": "n23-fence-b12-bs01",
    "n23-fence-b01-bs21": "n23-fence-b12-bs10",
    "n23-fence-b12-bs01": "n23-fence-b01-bs12",
    "n23-fence-b12-bs10": "n23-fence-b01-bs21",
}
assert all(dst == reciprocal[src] for src, dst in cellmap)
out = {
    "status": "PASS",
    "authority": "INDEPENDENT_REPLAY_CANDIDATE",
    "decides": [],
    "graph_effect": "NONE",
    "source_boundary": (
        "Hash-pinned retained records from the accepted independent census "
        "audit; no producer import and no recomputation of canonical digests."
    ),
    "manifest_sha256": hashlib.sha256(manifest_raw).hexdigest(),
    "bare_types": len(per_type),
    "actions": sum(primal.values()),
    "distinct_primal_digests": len(primal),
    "distinct_dual_digests": len(dual),
    "dual_multiset_equal": True,
    "cell_reciprocity": {f"{a}->{b}": n for (a, b), n in sorted(cellmap.items())},
}
(HERE / "duality-join.json").write_text(json.dumps(out, indent=2) + "\n",
                                         encoding="utf-8", newline="\n")
print(json.dumps(out, indent=2))
