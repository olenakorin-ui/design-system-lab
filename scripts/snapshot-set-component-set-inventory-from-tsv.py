#!/usr/bin/env python3
"""Merge component-set inventory TSV slices (id\\tname\\tpage) and set-inventory."""
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


def tsv_to_items(tsv: str) -> list[dict]:
    items: list[dict] = []
    for line in tsv.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            raise ValueError(f"expected id\\tname\\tpage, got {len(parts)} cols: {line[:80]}")
        iid, name, page = parts[0], parts[1], parts[2]
        items.append({"id": iid, "name": name, "page": page, "type": "COMPONENT_SET"})
    return items


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--expected", type=int, default=405)
    p.add_argument("tsv_files", nargs="+", type=Path)
    args = p.parse_args()
    merged: list[dict] = []
    for path in args.tsv_files:
        merged.extend(tsv_to_items(path.read_text(encoding="utf-8")))
    ids = [i["id"] for i in merged]
    if len(ids) != len(set(ids)):
        print("duplicate ids in merged inventory", file=sys.stderr)
        return 2
    if len(merged) != args.expected:
        print(f"count {len(merged)} != expected {args.expected}", file=sys.stderr)
        return 2
    out = {"items": merged}
    tmp = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging/component-sets-inventory.json"
    tmp.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    m = sbt.set_inventory("component-sets", merged, expected=args.expected)
    print(json.dumps({"inventoryCount": m["inventoryCount"], "complete": m["complete"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
