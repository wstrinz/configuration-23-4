"""Replay the actual CFG23 V4 exclusion proof objects with stdlib checkers.

This is a lane-local audit driver.  It does not import or invoke any producer.
The packet calls the target "Temperance 0.1.0", but no such named package is
present in the pinned workspace.  The revised scope below therefore names the
concrete independent checkers and proof-object joins that actually exist.
"""
from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CFG = HERE.parents[1]
V1 = CFG / "artifacts" / "fresh-look-real-order-v1"
V2 = CFG / "artifacts" / "signed-torus-push-v2"
Q = CFG / "artifacts" / "v4-b01-bs21-quotient-certificate-repair-v1"
RUNTIME_V2 = CFG / "artifacts" / "_temperance_replay_20260908_p2_runtime"
EVENTS = HERE / "events.jsonl"
SUMMARY = HERE / "summary.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def emit(obj: dict) -> None:
    with EVENTS.open("a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(obj, sort_keys=True) + "\n")


def run(label: str, command: list[str], cwd: Path) -> dict:
    started = time.monotonic()
    stamp = time.time()
    proc = subprocess.run(command, cwd=cwd, text=True, encoding="utf-8",
                          errors="replace", stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)
    elapsed = time.monotonic() - started
    log = HERE / f"{label}.log"
    log.write_text(proc.stdout, encoding="utf-8", newline="\n")
    rec = {"label": label, "command": command, "cwd": str(cwd),
           "started_unix": stamp, "wall_seconds": elapsed,
           "exit_code": proc.returncode, "log": log.name}
    emit({"event": "command", **rec})
    if proc.returncode:
        raise RuntimeError(f"{label} failed with exit code {proc.returncode}")
    return rec


def main() -> None:
    started = time.monotonic()
    EVENTS.write_text("", encoding="utf-8")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=CFG,
                                   text=True).strip()
    scope = {
        "requested_label": "Temperance 0.1.0",
        "named_package_located": False,
        "revision": (
            "Replay all concrete independent proof objects underlying the "
            "5,393 excluded action loci: six order-certificate batches, seven "
            "signed-torus batches, the 34 shared BS21 quotient-template "
            "certificates, all 980 continuation certificates, and the pinned "
            "coverage/duality joins.  The number 5,393 counts action loci, not "
            "one certificate file per action."
        ),
        "authority": "INDEPENDENT_REPLAY_CANDIDATE",
        "decides": [],
        "graph_effect": "NONE",
    }
    checkers = [V1 / "verify_order.py", V1 / "verify_torus.py",
                V2 / "verify_new.py", V2 / "verify_guard.py",
                Q / "code" / "check.py"]
    emit({"event": "start", "scope": scope, "git_head": head,
          "python": sys.version, "platform": platform.platform(),
          "checker_sha256": {str(p.relative_to(CFG)): sha256(p) for p in checkers}})

    commands: list[dict] = []
    receipts: list[dict] = []
    for cell in ("b01-bs01", "b01-bs10", "b01-bs12", "b01-bs21",
                 "b12-bs01", "b12-bs10"):
        out = HERE / f"verification_order_{cell}.json"
        commands.append(run(f"order_{cell}", [sys.executable, "-S",
            str(V1 / "verify_order.py"), "--input", f"certificates_{cell}.json",
            "--output", str(out), "--seconds", "1200", "--adversaries"], CFG))
        receipts.append(json.loads(out.read_text(encoding="utf-8")))

    for stem in ("bs01_sweep", "bs01_sweep2", "bs10_pilot", "bs10_sweep",
                 "bs10_sweep2", "bs12", "remaining30"):
        out = HERE / f"verification_torus_{stem}.json"
        commands.append(run(f"torus_{stem}", [sys.executable, "-S",
            str(V1 / "verify_torus.py"), "--input",
            f"torus_certificates_{stem}.json", "--output", str(out),
            "--seconds", "1200"], CFG))
        receipts.append(json.loads(out.read_text(encoding="utf-8")))

    commands.append(run("bs21_quotient_templates", [sys.executable, "-S", "check.py"],
                        Q / "code"))
    quotient = json.loads((Q / "output" / "check_report.json").read_text(encoding="utf-8"))

    if RUNTIME_V2.exists():
        raise RuntimeError(f"refusing to reuse runtime directory: {RUNTIME_V2}")
    RUNTIME_V2.mkdir()
    for p in V2.iterdir():
        if p.suffix in {".py", ".json", ".gz"} and p.is_file():
            shutil.copy2(p, RUNTIME_V2 / p.name)
    continuation = json.loads((V2 / "coverage.json").read_text(encoding="utf-8"))
    for item in continuation["verification_reports"]:
        cert = json.loads((V2 / item["file"]).read_text(encoding="utf-8"))["certificate_file"]
        checker = "verify_guard.py" if cert == "quadratic_guard.json" else "verify_new.py"
        label = "continuation_" + Path(cert).stem
        args = [sys.executable, "-S", checker, "--input", cert]
        if checker == "verify_new.py":
            args += ["--seconds", "1200"]
        commands.append(run(label, args, RUNTIME_V2))
        receipts.append(json.loads((RUNTIME_V2 / ("verification_" + cert)).read_text(encoding="utf-8")))

    commands.append(run("v1_coverage_join", [sys.executable, "-S",
                        str(V1 / "coverage_audit.py")], CFG))
    commands.append(run("v2_coverage_join", [sys.executable, "-S",
                        str(V2 / "audit_coverage.py")], CFG))

    per_certificate = []
    unresolved_rows = []
    for receipt in receipts:
        for r in receipt.get("results", []):
            row = {"pair_id": r.get("pair_id"), "status": r.get("status"),
                   "certificate_file": receipt.get("certificate_file")}
            per_certificate.append(row)
        for r in receipt.get("unresolved", []):
            unresolved_rows.append({"certificate_file": receipt.get("certificate_file"), **r})

    passed = {r["pair_id"] for r in per_certificate if r["status"] == "PASS"}
    positives = {r["pair_id"] for r in continuation["positives"]}
    terminal_unresolved = [r for r in unresolved_rows if r["pair_id"] not in passed]
    expected_positive_residuals = [r for r in terminal_unresolved if r["pair_id"] in positives]
    failures = [r for r in per_certificate if r["status"] != "PASS"]
    failures += [r for r in terminal_unresolved if r["pair_id"] not in positives]

    summary = {
        "status": "PASS" if (not failures and quotient.get("templates_passing") == 34
                              and quotient.get("actions_covered") == 453) else "FAIL",
        "scope": scope, "git_head": head,
        "wall_seconds": time.monotonic() - started,
        "commands": commands,
        "concrete_result_rows_replayed": len(per_certificate),
        "distinct_action_ids_in_direct_receipts": len({r["pair_id"] for r in per_certificate}),
        "failures": failures,
        "intermediate_unresolved_rows": unresolved_rows,
        "intermediate_unresolved_later_closed": len(unresolved_rows) - len(terminal_unresolved),
        "expected_positive_residuals": expected_positive_residuals,
        "bs21_shared_templates": {
            "templates_passing": quotient.get("templates_passing"),
            "actions_covered": quotient.get("actions_covered"),
            "all_pass": quotient.get("ALL_PASS"),
        },
        "declared_final_action_count": continuation["total_actions"],
        "declared_excluded_action_count": continuation["total_excluded"],
        "declared_realized_action_count": continuation["realized_actions"],
        "note": (
            "Per-certificate rows cover direct proof records. Shared template "
            "certificates and duality transports make the final action-locus "
            "count a coverage join rather than a one-row-per-certificate count."
        ),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8", newline="\n")
    emit({"event": "finish", "summary": SUMMARY.name, "status": summary["status"],
          "wall_seconds": summary["wall_seconds"]})
    print(json.dumps({k: summary[k] for k in ("status", "wall_seconds",
          "concrete_result_rows_replayed", "distinct_action_ids_in_direct_receipts",
          "failures")}, indent=2))


if __name__ == "__main__":
    main()
