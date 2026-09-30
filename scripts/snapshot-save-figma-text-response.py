#!/usr/bin/env python3
"""Write use_figma text batch JSON from stdin to staging text-{index}.mcp.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: snapshot-save-figma-text-response.py INDEX", file=sys.stderr)
        return 2
    idx = int(sys.argv[1])
    data = json.load(sys.stdin)
    STAGING.mkdir(parents=True, exist_ok=True)
    out = STAGING / f"text-{idx}.mcp.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
