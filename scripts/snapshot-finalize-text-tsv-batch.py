#!/usr/bin/env python3
"""Build text-{index}.mcp.json from staging TSV + metadata and run ingest."""
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
    args = p.parse_args()
    tsv_path = STAGING / f"text-{args.index}.tsv"
    if not tsv_path.is_file():
        print(f"REJECTED: missing {tsv_path}", file=sys.stderr)
        return 3
    tsv = tsv_path.read_text(encoding="utf-8")
    data = {
        "start": args.start,
        "end": args.end,
        "count": args.count,
        "total": args.total,
        "tsv": tsv,
    }
    mcp_path = STAGING / f"text-{args.index}.mcp.json"
    mcp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cmd = [
        sys.executable,
        str(ROOT / "scripts/snapshot-ingest-tsv.py"),
        "--category",
        "text-styles",
        "--index",
        str(args.index),
        "--requested",
        str(args.requested),
        "--tsv-file",
        str(tsv_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
