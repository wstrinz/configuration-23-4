"""Run the same saturated-ideal pipeline on Cuntz-22 and 3 exclusions."""
from __future__ import annotations

import hashlib
import json
import random
import subprocess
import sys
from pathlib import Path

import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
OLD = ROOT / "artifacts/fresh-look-real-order-v1"
V2 = ROOT / "artifacts/signed-torus-push-v2"
PINS = ROOT / "artifacts/v4-complete-action-pair-census-v1/output/stage2_pair_pins"
sys.path.insert(0, str(OLD))
import order_probe
import torus_certify


def saturated_basis(polys, variables):
    u = sp.Symbol("u")
    gb = sp.groebner([*polys, u * sp.prod(variables) - 1], u, *variables,
                     order="lex", domain=sp.QQ)
    return [sp.Poly(p, *variables, domain=sp.QQ).monic().as_expr()
            for p in gb.polys if u not in p.free_symbols]


def singular_check(label, polys, variables):
    names = ",".join(["u", *map(str, variables)])
    rendered = [str(p).replace("**", "^") for p in polys]
    text = f'''ring r=0,({names}),lp;
ideal K={','.join(rendered + ['u*' + '*'.join(map(str, variables)) + '-1'])};
ideal G=std(K);
ideal J=eliminate(G,u);
ring s=0,({','.join(map(str, variables))}),lp;
ideal J=imap(r,J);
print("{label}"); print(dim(std(J))); print(vdim(std(J))); print(std(J));
'''
    path = HERE / f"control_{label.lower()}_singular.sing"
    path.write_bytes(text.encode())
    p = path.resolve().as_posix(); wsl = f"/mnt/{p[0].lower()}{p[2:]}"
    proc = subprocess.run(["wsl", "bash", "-lc", f"Singular {wsl}"], text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = HERE / f"control_{label.lower()}_singular.out"
    out.write_bytes(proc.stdout.encode())
    assert proc.returncode == 0
    return {"input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "output_sha256": hashlib.sha256(out.read_bytes()).hexdigest()}


def main():
    all_pins = {p["pair_id"]: p for path in PINS.glob("*.json") for p in json.loads(path.read_text())}
    coverage = json.loads((V2 / "coverage.json").read_text())
    positive_ids = {p["pair_id"] for p in coverage["positives"]}
    excluded = sorted(set(all_pins) - positive_ids)
    assert len(excluded) == 5393
    rng = random.Random(2304)
    sampled = rng.sample(excluded, 3)
    blobs = order_probe.read_blobs([all_pins[p]["source_blob_sha1"] for p in sampled])

    jobs = [("CUNTZ22", order_probe.control(), None)]
    for i, pair_id in enumerate(sampled, 1):
        pin = all_pins[pair_id]
        obj = json.loads(blobs[pin["source_blob_sha1"]])
        gp = order_probe.permutations(*(tuple(bytes.fromhex(g)) for g in pin["subgroup_generators_points"]))
        jobs.append((f"NEG{i}", order_probe.compile_action(obj["lines"], gp), pair_id))

    result = {"authority": "EXACT_COMPUTATION", "decides": [], "graph_effect": "NONE",
              "negative_sample_seed": 2304, "negative_population": len(excluded), "cases": []}
    for label, model, pair_id in jobs:
        _, variables, polys = torus_certify.torus_map(model)
        basis = saturated_basis(polys, variables)
        singular = singular_check(label, polys, variables)
        unit = len(basis) == 1 and basis[0] == 1
        row = {"label": label, "pair_id": pair_id, "variables": len(variables),
               "equations": len(polys), "sympy_saturated_basis": list(map(str, basis)),
               "sympy_empty_open_torus": unit, "singular": singular}
        if label == "CUNTZ22":
            assert not unit
        else:
            assert unit
            sources = []
            if pair_id in coverage["exclusion_sources"]:
                sources.extend(coverage["exclusion_sources"][pair_id])
            for path in OLD.glob("verification*.json"):
                data = json.loads(path.read_text())
                if any(r.get("pair_id") == pair_id for r in data.get("results", [])):
                    sources.append(path.name)
            assert sources
            row["certificate_sources"] = sorted(set(sources))
        result["cases"].append(row)
        print(label, "unit ideal" if unit else "nonempty", flush=True)
    result["generator_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE / "controls_receipt.json").write_bytes((json.dumps(result, indent=2) + "\n").encode())


if __name__ == "__main__":
    main()
