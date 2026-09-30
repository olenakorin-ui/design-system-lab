#!/usr/bin/env python3
"""Convert cs-inv-part-{n}.b64 (items JSON b64) to cs-inv-part-{n}.json."""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--staging", type=Path, default=STAGING)
    p.add_argument("--parts", type=int, nargs="*", default=[0, 1, 2, 3])
    args = p.parse_args()
    total = 0
    for i in args.parts:
        b64_path = args.staging / f"cs-inv-part-{i}.b64"
        if not b64_path.exists():
            raise SystemExit(f"missing {b64_path}")
        b64 = b64_path.read_text(encoding="utf-8").strip()
        items = json.loads(base64.b64decode(b64).decode("utf-8"))
        out = args.staging / f"cs-inv-part-{i}.json"
        out.write_text(json.dumps({"items": items}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        mcp = {"part": i, "count": len(items), "itemsB64": b64}
        (args.staging / f"cs-inv-part-{i}.mcp.json").write_text(
            json.dumps(mcp, indent=2) + "\n", encoding="utf-8"
        )
        total += len(items)
        print(i, len(items))
    print("total", total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
