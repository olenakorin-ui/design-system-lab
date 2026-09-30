#!/usr/bin/env python3
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "design-system/snapshots/_raw/mcp"
parts = json.loads((ROOT / "scripts/_tmp_idx0_parts.json").read_text())
b64 = parts["p0"] + parts["p1"] + parts["p2"]
data = json.loads(base64.b64decode(b64).decode("utf-8"))
out = MCP / "component-sets-index.batch-0.json"
out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(data))
