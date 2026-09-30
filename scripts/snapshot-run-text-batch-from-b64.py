#!/usr/bin/env python3
"""Create MCP JSON from tsvB64 file + metadata, then decode+ingest."""
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
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--start", type=int, required=True)
    p.add_argument("--end", type=int, required=True)
    p.add_argument("--count", type=int, required=True)
    p.add_argument("--total", type=int, default=309)
    p.add_argument("--b64-file", type=Path, required=True)
    args = p.parse_args()
    data = {
        "start": args.start,
        "end": args.end,
        "count": args.count,
        "total": args.total,
        "tsvB64": args.b64_file.read_text(encoding="utf-8").strip(),
    }
    STAGING.mkdir(parents=True, exist_ok=True)
    mcp_path = STAGING / f"text-{args.index}.mcp.json"
    mcp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cmd = [
        sys.executable,
        str(ROOT / "scripts/snapshot-decode-text-tsv-b64.py"),
        "--index",
        str(args.index),
        "--requested",
        str(args.requested),
        "--mcp-json",
        str(mcp_path),
    ]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
