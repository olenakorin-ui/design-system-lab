#!/usr/bin/env python3
"""Save a JSON array/object from argv[1] file path (raw json string) to argv[2] output path."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: save-mcp-batch.py <input.json> <output.json>", file=sys.stderr)
        return 2
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    obj = json.loads(src.read_text(encoding="utf-8"))
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(obj) if isinstance(obj, list) else "ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
