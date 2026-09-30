#!/usr/bin/env python3
"""Build text-styles inventory from ids + names JSON files and set-inventory."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ids-file", type=Path, required=True)
    p.add_argument("--names-file", type=Path, nargs="+", required=True)
    p.add_argument("--expected", type=int, default=309)
    args = p.parse_args()
    ids_data = json.loads(args.ids_file.read_text(encoding="utf-8"))
    ids = ids_data["ids"] if isinstance(ids_data, dict) else ids_data
    names: list[str] = []
    for nf in args.names_file:
        nd = json.loads(nf.read_text(encoding="utf-8"))
        names.extend(nd["names"] if isinstance(nd, dict) else nd)
    if len(ids) != len(names):
        print(f"ids {len(ids)} != names {len(names)}", file=sys.stderr)
        return 2
    items = [{"id": i, "name": n, "type": "TEXT"} for i, n in zip(ids, names)]
    out = ROOT / "design-system/snapshots/_raw/batches/inventories/text-styles.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"category": "text-styles", "count": len(items), "items": items}, indent=2) + "\n", encoding="utf-8")
    spec = importlib.util.spec_from_file_location("sbt", ROOT / "scripts/snapshot-batch-tools.py")
    sbt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sbt)
    m = sbt.set_inventory("text-styles", items, expected=args.expected)
    print(json.dumps({"inventoryCount": m["inventoryCount"], "complete": m["complete"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
