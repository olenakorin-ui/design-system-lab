#!/usr/bin/env python3
"""Merge TSV-in-b64 text style inventory slices and set-inventory."""
from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def tsv_to_items(tsv: str) -> list[dict]:
    items = []
    for line in tsv.strip().splitlines():
        if not line.strip():
            continue
        iid, name = line.split("\t", 1)
        items.append({"id": iid, "name": name, "type": "TEXT"})
    return items


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--expected", type=int, default=309)
    p.add_argument("b64_files", nargs="+", type=Path)
    args = p.parse_args()
    merged: list[dict] = []
    for path in args.b64_files:
        b64 = path.read_text(encoding="utf-8").strip()
        tsv = base64.b64decode(b64).decode("utf-8")
        merged.extend(tsv_to_items(tsv))
    ids = [i["id"] for i in merged]
    if len(ids) != len(set(ids)):
        print("duplicate ids in merged inventory", file=sys.stderr)
        return 2
    if len(merged) != args.expected:
        print(f"count {len(merged)} != expected {args.expected}", file=sys.stderr)
        return 3
    out = STAGING / "text-styles-inventory.json"
    out.write_text(json.dumps({"items": merged}, indent=2) + "\n", encoding="utf-8")
    spec = importlib.util.spec_from_file_location("sbt", ROOT / "scripts/snapshot-batch-tools.py")
    sbt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sbt)
    m = sbt.set_inventory("text-styles", merged, expected=args.expected)
    print(json.dumps({"inventoryCount": m["inventoryCount"], "complete": m["complete"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
