#!/usr/bin/env python3
"""Write cs-inv-{index}.tsv and .mcp.json from a use_figma response JSON file."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--response", type=Path, required=True, help="JSON with tsv field")
    args = p.parse_args()
    data = json.loads(args.response.read_text(encoding="utf-8"))
    tsv = data.get("tsv") or ""
    if not tsv.strip():
        raise SystemExit("missing or empty tsv in response")
    STAGING.mkdir(parents=True, exist_ok=True)
    tsv_path = STAGING / f"cs-inv-{args.index}.tsv"
    mcp_path = STAGING / f"cs-inv-{args.index}.mcp.json"
    tsv_path.write_text(tsv if tsv.endswith("\n") else tsv + "\n", encoding="utf-8")
    mcp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = len([ln for ln in tsv.splitlines() if ln.strip()])
    print(json.dumps({"index": args.index, "lines": lines, "expectedCount": data.get("count")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
