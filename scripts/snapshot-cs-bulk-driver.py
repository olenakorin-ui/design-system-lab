#!/usr/bin/env python3
"""List pending CS detail batches and emit use_figma code paths for automation."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging/cs-detail-queue.json"
MANIFEST = ROOT / "design-system/snapshots/_raw/batches/component-sets/manifest.json"
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def pending_batches(limit: int = 10) -> list[dict]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    done = set(manifest.get("completedBatches") or [])
    missing = set(manifest.get("missingIds") or [])
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))["queue"]
    out = []
    for entry in queue:
        idx = entry["index"]
        if idx in done:
            continue
        ids = [i for i in entry["ids"] if i in missing]
        if not ids:
            continue
        out.append({"index": idx, "ids": ids, "requested": len(ids)})
        if len(out) >= limit:
            break
    return out


def main() -> int:
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    batches = pending_batches(limit)
    STAGING.mkdir(parents=True, exist_ok=True)
    for b in batches:
        code_path = STAGING / f"cs-code-{b['index']:04d}.js"
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts" / "snapshot-cs-pack-code.py"),
                "--tsv",
                "--ids",
                *b["ids"],
            ],
            check=True,
            stdout=code_path.open("w", encoding="utf-8"),
        )
    print(json.dumps({"pending": batches, "count": len(batches)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
