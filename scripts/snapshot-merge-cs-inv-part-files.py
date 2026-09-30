#!/usr/bin/env python3
"""Merge cs-inv-part-*.json slices and set component-sets inventory."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"
spec = importlib.util.spec_from_file_location("sbt", ROOT / "scripts" / "snapshot-batch-tools.py")
sbt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbt)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--expected", type=int, default=405)
    p.add_argument("--staging", type=Path, default=STAGING)
    args = p.parse_args()
    merged: list[dict] = []
    for path in sorted(args.staging.glob("cs-inv-part-*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        merged.extend(data.get("items") or [])
    ids = [i["id"] for i in merged]
    if len(ids) != len(set(ids)):
        print("duplicate ids", file=sys.stderr)
        return 2
    if len(merged) != args.expected:
        print(f"count {len(merged)} != expected {args.expected}", file=sys.stderr)
        return 2
    items = [
        {"id": i["id"], "name": i["name"], "page": i.get("page", ""), "type": "COMPONENT_SET"}
        for i in merged
    ]
    m = sbt.set_inventory("component-sets", items, expected=args.expected)
    print(json.dumps({"inventoryCount": m["inventoryCount"], "complete": m["complete"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
