"""Hash the retained P1 sources and receipts."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
rows = []
for path in sorted(HERE.iterdir()):
    if not path.is_file() or path.name == "manifest.json":
        continue
    raw = path.read_bytes()
    rows.append({"path": path.name, "bytes": len(raw),
                 "sha256": hashlib.sha256(raw).hexdigest()})
(HERE / "manifest.json").write_bytes((json.dumps({
    "authority": "EXACT_COMPUTATION", "decides": [], "graph_effect": "NONE",
    "files": rows}, indent=2) + "\n").encode())
