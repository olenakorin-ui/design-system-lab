#!/usr/bin/env python3
"""Write MCP use_figma batch response JSON to staging b64 and run snapshot-ingest-b64."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--category", required=True)
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--response-file", type=Path, required=True, help="JSON {count,b64,...}")
    args = p.parse_args()
    data = json.loads(args.response_file.read_text(encoding="utf-8"))
    b64 = data["b64"]
    count = int(data.get("count", -1))
    b64_path = STAGING / f"{args.category}-{args.index}.b64"
    b64_path.parent.mkdir(parents=True, exist_ok=True)
    b64_path.write_text(b64, encoding="utf-8")
    cmd = [
        sys.executable,
        str(ROOT / "scripts/snapshot-ingest-b64.py"),
        "--category",
        args.category,
        "--index",
        str(args.index),
        "--requested",
        str(args.requested),
        "--b64-file",
        str(b64_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return proc.returncode
    meta = json.loads(proc.stdout)
    if meta.get("receivedCount") != count:
        print(f"WARN: MCP count {count} != ingested {meta.get('receivedCount')}", file=sys.stderr)
    print(json.dumps({"ingest": meta, "mcpCount": count}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
