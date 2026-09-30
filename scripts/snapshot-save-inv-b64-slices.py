#!/usr/bin/env python3
"""Save text inventory TSV b64 slices from MCP JSON files in _staging."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def main() -> int:
    for i, name in enumerate(("text-inv-resp-0.json", "text-inv-resp-1.json", "text-inv-resp-2.json", "text-inv-resp-3.json")):
        path = STAGING / name
        if not path.exists():
            print(f"missing {path}", file=sys.stderr)
            return 2
        data = json.loads(path.read_text(encoding="utf-8"))
        out = STAGING / f"text-inv-{i}.b64"
        out.write_text(data["b64"], encoding="utf-8")
        print(f"wrote {out.name} count={data.get('count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
