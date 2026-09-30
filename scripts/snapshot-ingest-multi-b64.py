#!/usr/bin/env python3
"""Ingest multiple b64 batches from JSON stdin: {"batches":[{"index", "requested", "count", "b64"}, ...]}."""
from __future__ import annotations

import base64
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def main() -> int:
    data = json.load(sys.stdin)
    category = data["category"]
    results = []
    for b in data["batches"]:
        idx = int(b["index"])
        requested = int(b["requested"])
        b64_path = STAGING / f"{category}-{idx}.b64"
        b64_path.write_text(b["b64"], encoding="utf-8")
        items = json.loads(base64.b64decode(b["b64"]).decode("utf-8"))
        if len(items) != int(b["count"]):
            print(f"REJECT batch {idx}: count mismatch {len(items)} vs {b['count']}", file=sys.stderr)
            return 3
        cmd = [
            sys.executable,
            str(ROOT / "scripts/snapshot-ingest-b64.py"),
            "--category",
            category,
            "--index",
            str(idx),
            "--requested",
            str(requested),
            "--b64-file",
            str(b64_path),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            print(proc.stderr or proc.stdout, file=sys.stderr)
            return proc.returncode
        results.append(json.loads(proc.stdout))
    print(json.dumps({"ingested": len(results), "batches": results}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
