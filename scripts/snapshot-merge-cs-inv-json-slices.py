#!/usr/bin/env python3
"""Merge component-set inventory JSON slices ({items:[{id,name,page}]}) and set-inventory."""
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
    p.add_argument("json_files", nargs="+", type=Path)
    args = p.parse_args()
    merged: list[dict] = []
    for path in args.json_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        chunk = data.get("items") if isinstance(data, dict) else data
        for item in chunk:
            merged.append(
                {
                    "id": item["id"],
                    "name": item["name"],
                    "page": item.get("page", ""),
                    "type": "COMPONENT_SET",
                }
            )
    ids = [i["id"] for i in merged]
    if len(ids) != len(set(ids)):
        print("duplicate ids", file=sys.stderr)
        return 2
    if len(merged) != args.expected:
        print(f"count {len(merged)} != expected {args.expected}", file=sys.stderr)
        return 2
    out_path = ROOT / "design-system/snapshots/_raw/batches/inventories/component-sets.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    m = sbt.set_inventory("component-sets", merged, expected=args.expected)
    print(json.dumps({"inventoryCount": m["inventoryCount"], "complete": m["complete"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
