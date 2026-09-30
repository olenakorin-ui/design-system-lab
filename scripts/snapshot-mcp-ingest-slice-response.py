#!/usr/bin/env python3
"""Ingest one MCP slice response JSON file into snapshot-mcp-batch-b64-slice."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--category", required=True)
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--response-file", type=Path, required=True)
    args = p.parse_args()
    data = json.loads(args.response_file.read_text(encoding="utf-8"))
    slice_path = args.response_file.with_suffix(".slice.txt")
    slice_path.write_text(data["slice"], encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/snapshot-mcp-batch-b64-slice.py"),
            "--category",
            args.category,
            "--index",
            str(args.index),
            "--requested",
            str(args.requested),
            "--part-index",
            str(int(data["partIndex"])),
            "--total-parts",
            str(int(data["totalParts"])),
            "--expected-b64-len",
            str(int(data["expectedB64Len"])),
            "--mcp-count",
            str(int(data["count"])),
            "--slice-file",
            str(slice_path),
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return proc.returncode
    print(proc.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
