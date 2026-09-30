#!/usr/bin/env python3
"""Write text-style TSV + MCP JSON staging files from a single-batch use_figma response."""
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
    p.add_argument("--mcp-json", type=Path, required=True, help="Full use_figma JSON response file")
    p.add_argument("--ingest", action="store_true", default=True)
    p.add_argument("--no-ingest", action="store_false", dest="ingest")
    args = p.parse_args()
    data = json.loads(args.mcp_json.read_text(encoding="utf-8"))
    if "tsv" not in data:
        print("REJECTED: missing tsv field", file=sys.stderr)
        return 3
    STAGING.mkdir(parents=True, exist_ok=True)
    tsv_path = STAGING / f"text-{args.index}.tsv"
    mcp_path = STAGING / f"text-{args.index}.mcp.json"
    tsv_path.write_text(data["tsv"], encoding="utf-8")
    mcp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if not args.ingest:
        print(json.dumps({"tsv": str(tsv_path), "mcp": str(mcp_path), "count": data.get("count")}))
        return 0
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
