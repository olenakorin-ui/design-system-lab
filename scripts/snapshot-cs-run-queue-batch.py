#!/usr/bin/env python3
"""Prepare / ingest one component-set queue batch from saved MCP JSON."""
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
    p.add_argument("--ids", nargs="+", required=True)
    p.add_argument("--write-code-only", action="store_true")
    p.add_argument("--ingest-response", type=Path)
    args = p.parse_args()
    code_path = STAGING / f"cs-code-{args.index:04d}.js"
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "snapshot-cs-pack-code.py"), "--tsv", "--ids", *args.ids],
        capture_output=True,
        text=True,
        check=True,
    )
    code_path.write_text(proc.stdout, encoding="utf-8")
    if args.write_code_only:
        print(json.dumps({"index": args.index, "requested": len(args.ids), "codeFile": str(code_path)}))
        return 0
    if not args.ingest_response:
        print(json.dumps({"index": args.index, "requested": len(args.ids), "codeFile": str(code_path), "needMcp": True}))
        return 0
    ingest = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "snapshot-ingest-cs-figma-response.py"),
            "--index",
            str(args.index),
            "--requested",
            str(len(args.ids)),
            "--response-file",
            str(args.ingest_response),
        ],
        capture_output=True,
        text=True,
    )
    if ingest.returncode != 0:
        sys.stderr.write(ingest.stderr)
        return ingest.returncode
    print(ingest.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
