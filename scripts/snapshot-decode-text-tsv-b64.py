#!/usr/bin/env python3
"""Decode Figma tsvB64 (btoa(unescape(encodeURIComponent(tsv)))) and persist + ingest."""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def figma_b64_to_text(b64: str) -> str:
    raw = base64.b64decode(b64)
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("latin-1")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--mcp-json", type=Path, help="MCP response JSON with tsv or tsvB64")
    p.add_argument("--stdin-json", action="store_true", help="Read use_figma JSON from stdin")
    p.add_argument("--b64-file", type=Path, help="Raw base64 file")
    p.add_argument("--start", type=int, default=None)
    p.add_argument("--end", type=int, default=None)
    p.add_argument("--count", type=int, default=None)
    p.add_argument("--total", type=int, default=309)
    args = p.parse_args()
    if args.stdin_json:
        data = json.load(sys.stdin)
    elif args.mcp_json:
        data = json.loads(args.mcp_json.read_text(encoding="utf-8"))
    else:
        data = {}
    b64 = data.get("tsvB64")
    if b64 is None and args.b64_file:
        b64 = args.b64_file.read_text(encoding="utf-8").strip()
        if args.start is not None:
            data.setdefault("start", args.start)
            data.setdefault("end", args.end)
            data.setdefault("count", args.count)
            data.setdefault("total", args.total)
            data["tsvB64"] = b64
    if not b64:
        print("REJECTED: no tsvB64", file=sys.stderr)
        return 3
    tsv = figma_b64_to_text(b64)
    if "tsv" not in data:
        data["tsv"] = tsv
    STAGING.mkdir(parents=True, exist_ok=True)
    tsv_path = STAGING / f"text-{args.index}.tsv"
    mcp_path = STAGING / f"text-{args.index}.mcp.json"
    tsv_path.write_text(tsv, encoding="utf-8")
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
