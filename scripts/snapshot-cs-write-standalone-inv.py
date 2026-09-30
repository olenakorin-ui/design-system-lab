#!/usr/bin/env python3
"""Decode standalone-components tsvB64 and set components inventory."""
from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sbt", ROOT / "scripts" / "snapshot-batch-tools.py")
sbt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbt)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--b64-file", type=Path, required=True)
    args = p.parse_args()
    tsv = base64.b64decode(args.b64_file.read_text(encoding="utf-8").strip()).decode("utf-8")
    items = []
    for line in tsv.strip().splitlines():
        if not line.strip():
            continue
        sid, name, page = line.split("\t", 2)
        items.append({"id": sid, "name": name, "type": "COMPONENT", "page": page})
    out = ROOT / "design-system/snapshots/_raw/batches/inventories/components.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps({"category": "components", "count": len(items), "items": items}, indent=2) + "\n",
        encoding="utf-8",
    )
    m = sbt.set_inventory("components", items)
    print(json.dumps({"inventoryCount": m["inventoryCount"], "complete": m["complete"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
