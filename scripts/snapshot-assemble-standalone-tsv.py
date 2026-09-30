#!/usr/bin/env python3
"""Append TSV slice parts from staging and set components inventory."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"
spec = importlib.util.spec_from_file_location("sbt", ROOT / "scripts" / "snapshot-batch-tools.py")
sbt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbt)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--key", default="standalone-components")
    p.add_argument("--total-parts", type=int, required=True)
    p.add_argument("--expected-len", type=int, required=True)
    p.add_argument("--expected-rows", type=int, required=True)
    args = p.parse_args()
    parts = []
    for i in range(args.total_parts):
        path = STAGING / f"{args.key}.tsv.part-{i:03d}.txt"
        if not path.exists():
            print(f"missing {path}", file=sys.stderr)
            return 2
        parts.append(path.read_text(encoding="utf-8"))
    tsv = "".join(parts)
    if len(tsv) != args.expected_len:
        print(f"len mismatch {len(tsv)} != {args.expected_len}", file=sys.stderr)
        return 3
    rows = [ln for ln in tsv.splitlines() if ln.strip()]
    if len(rows) != args.expected_rows:
        print(f"row mismatch {len(rows)} != {args.expected_rows}", file=sys.stderr)
        return 4
    items = []
    for line in rows:
        sid, name, page = line.split("\t", 2)
        items.append({"id": sid, "name": name, "type": "COMPONENT", "page": page})
    out_tsv = STAGING / f"{args.key}.tsv"
    out_tsv.write_text(tsv + "\n", encoding="utf-8")
    m = sbt.set_inventory("components", items)
    print(json.dumps({"inventoryCount": m["inventoryCount"], "complete": m["complete"], "tsv": str(out_tsv)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
