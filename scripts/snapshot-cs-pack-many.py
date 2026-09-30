#!/usr/bin/env python3
"""Print use_figma JS to pack up to N missing component-sets from the queue."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging/cs-detail-queue.json"
MANIFEST = ROOT / "design-system/snapshots/_raw/batches/component-sets/manifest.json"


def collect_ids(max_ids: int) -> tuple[list[str], int, int]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    done = set(manifest.get("completedBatches") or [])
    missing = set(manifest.get("missingIds") or [])
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))["queue"]
    ids: list[str] = []
    start_index = None
    end_index = None
    for entry in queue:
        idx = entry["index"]
        if idx in done:
            continue
        batch_ids = [i for i in entry["ids"] if i in missing]
        if not batch_ids:
            continue
        if start_index is None:
            start_index = idx
        for bid in batch_ids:
            if bid not in ids:
                ids.append(bid)
                end_index = idx
                if len(ids) >= max_ids:
                    return ids, start_index, end_index
    if start_index is None:
        return [], 0, 0
    return ids, start_index, end_index


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--max-ids", type=int, default=24)
    args = p.parse_args()
    ids, start_idx, end_idx = collect_ids(args.max_ids)
    if not ids:
        print(json.dumps({"done": True}))
        return 0
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "snapshot-cs-pack-code.py"), "--tsv", "--ids", *ids],
        capture_output=True,
        text=True,
        check=True,
    )
    meta = {
        "ids": ids,
        "count": len(ids),
        "startBatchIndex": start_idx,
        "endBatchIndex": end_idx,
        "linesPerBatch": 8,
    }
    out = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging/cs-pack-many-meta.json"
    out.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    sys.stdout.write(proc.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
