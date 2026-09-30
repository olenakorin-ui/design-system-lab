#!/usr/bin/env python3
"""set-inventory for component-sets from a single MCP JSON {total, items:[...]}."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sbt", ROOT / "scripts" / "snapshot-batch-tools.py")
sbt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbt)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--expected", type=int, default=405)
    p.add_argument("--mcp-json", type=Path, help="JSON file with items array")
    p.add_argument("--stdin-json", action="store_true")
    args = p.parse_args()
    if args.stdin_json:
        data = json.load(sys.stdin)
    else:
        data = json.loads(args.mcp_json.read_text(encoding="utf-8"))
    items_in = data.get("items") or data
    merged = [
        {
            "id": i["id"],
            "name": i["name"],
            "page": i.get("page", ""),
            "type": "COMPONENT_SET",
        }
        for i in items_in
    ]
    if len(merged) != args.expected:
        print(f"count {len(merged)} != expected {args.expected}", file=sys.stderr)
        return 2
    m = sbt.set_inventory("component-sets", merged, expected=args.expected)
    print(json.dumps({"inventoryCount": m["inventoryCount"], "complete": m["complete"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
