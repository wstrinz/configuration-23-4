"""Run the exported systems through Singular and msolve and retain receipts."""
from __future__ import annotations

import hashlib
import json
import subprocess
import time
from pathlib import Path


HERE = Path(__file__).resolve().parent
MSOLVE = "/mnt/c/tmp/msolve-0.10.1-linux-x86/msolve"


def write_text_lf(path, value):
    path.write_bytes(value.encode())


def wsl_path(path: Path) -> str:
    p = path.resolve().as_posix()
    assert len(p) > 2 and p[1] == ":"
    return f"/mnt/{p[0].lower()}{p[2:]}"


def run(command):
    start = time.monotonic()
    proc = subprocess.run(["wsl", "bash", "-lc", command], text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, time.monotonic() - start, proc.stdout


def main():
    receipt = {"authority": "EXACT_COMPUTATION", "decides": [], "graph_effect": "NONE", "runs": []}
    for name in ("e1", "e2"):
        singular_in = HERE / f"{name}_singular.sing"
        code, seconds, output = run(f"Singular {wsl_path(singular_in)}")
        write_text_lf(HERE / f"{name}_singular.out", output)
        assert code == 0 and "SATURATED_DIM" in output and "PRIMARY_COMPONENT_COUNT" in output, output
        receipt["runs"].append({"case": name.upper(), "solver": "Singular", "command": f"Singular {singular_in.name}",
                                "exit_code": code, "seconds": seconds,
                                "input_sha256": hashlib.sha256(singular_in.read_bytes()).hexdigest(),
                                "output_sha256": hashlib.sha256(output.encode()).hexdigest()})

        msolve_in = HERE / f"{name}_msolve.in"
        msolve_out = HERE / f"{name}_msolve.out"
        code, seconds, output = run(f"{MSOLVE} -f {wsl_path(msolve_in)} -o {wsl_path(msolve_out)} -v 1")
        write_text_lf(HERE / f"{name}_msolve.log", output)
        assert code == 0 and msolve_out.exists(), output
        receipt["runs"].append({"case": name.upper(), "solver": "msolve 0.10.1", "command": f"msolve -f {msolve_in.name} -o {msolve_out.name} -v 1",
                                "exit_code": code, "seconds": seconds,
                                "input_sha256": hashlib.sha256(msolve_in.read_bytes()).hexdigest(),
                                "output_sha256": hashlib.sha256(msolve_out.read_bytes()).hexdigest(),
                                "log_sha256": hashlib.sha256(output.encode()).hexdigest()})
    receipt["generator_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    write_text_lf(HERE / "external_solver_receipt.json", json.dumps(receipt, indent=2) + "\n")


if __name__ == "__main__":
    main()
