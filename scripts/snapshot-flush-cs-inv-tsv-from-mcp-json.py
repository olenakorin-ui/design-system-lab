#!/usr/bin/env python3
"""Write cs-inv-s60-{start}.tsv from JSON files containing {start, tsv, count}."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("mcp_json_files", nargs="+", type=Path)
    args = p.parse_args()
    STAGING.mkdir(parents=True, exist_ok=True)
    total = 0
    for path in args.mcp_json_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        start = int(data["start"])
        tsv = data.get("tsv") or ""
        if not tsv.strip():
            print(f"empty tsv in {path}", file=sys.stderr)
            return 2
        out = STAGING / f"cs-inv-s60-{start}.tsv"
        out.write_text(tsv if tsv.endswith("\n") else tsv + "\n", encoding="utf-8")
        mcp_out = STAGING / f"cs-inv-s60-{start}.mcp.json"
        mcp_out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        n = len([ln for ln in tsv.splitlines() if ln.strip()])
        total += n
        print(start, n, data.get("count"))
    print("total_lines", total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
