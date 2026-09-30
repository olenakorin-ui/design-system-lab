#!/usr/bin/env python3
"""Write a component-sets batch from a JSON file containing an items array."""
from __future__ import annotations

import argparse
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
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--items-file", type=Path, required=True)
    args = p.parse_args()
    data = json.loads(args.items_file.read_text(encoding="utf-8"))
    items = data["items"] if isinstance(data, dict) and "items" in data else data
    meta = sbt.write_batch(
        "component-sets",
        args.index,
        items,
        requested_count=args.requested,
    )
    print(json.dumps(meta))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
