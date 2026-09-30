#!/usr/bin/env python3
"""Ingest one text batch from staging text-{index}.mcp.json (tsv or tsvB64)."""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    args = p.parse_args()
    mcp = STAGING / f"text-{args.index}.mcp.json"
    if not mcp.exists():
        print(f"REJECTED: missing {mcp}", file=sys.stderr)
        return 3
    cmd = [
        sys.executable,
        str(ROOT / "scripts/snapshot-decode-text-tsv-b64.py"),
        "--index",
        str(args.index),
        "--requested",
        str(args.requested),
        "--mcp-json",
        str(mcp),
    ]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
