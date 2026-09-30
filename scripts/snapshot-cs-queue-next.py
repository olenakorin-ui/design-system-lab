#!/usr/bin/env python3
"""Print next pending component-set detail batch from cs-detail-queue.json."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging/cs-detail-queue.json"
MANIFEST = ROOT / "design-system/snapshots/_raw/batches/component-sets/manifest.json"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--code", action="store_true", help="Print use_figma JS (--tsv by default)")
    p.add_argument("--tsv", action="store_true", default=True)
    p.add_argument("--no-tsv", action="store_true")
    args = p.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    done = set(manifest.get("completedBatches") or [])
    missing = set(manifest.get("missingIds") or [])
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))["queue"]
    pending = None
    for entry in queue:
        idx = entry["index"]
        if idx in done:
            continue
        ids = [i for i in entry["ids"] if i in missing]
        if not ids:
            continue
        pending = {"index": idx, "ids": ids, "requested": len(ids)}
        break
    if not pending:
        print(json.dumps({"done": True, "missing": len(missing)}))
        return 0
    print(json.dumps(pending))
    if args.code:
        import subprocess
        import sys

        tsv_flag = ["--tsv"] if not args.no_tsv else []
        subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "snapshot-cs-pack-code.py"), *tsv_flag, "--ids", *pending["ids"]],
            check=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
