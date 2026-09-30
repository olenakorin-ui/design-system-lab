#!/usr/bin/env python3
"""Write JSON object to path (argv[1]). Reads JSON from argv[2] file if present, else stdin."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: write-mcp-json.py <out.json> [input.json]", file=sys.stderr)
        return 2
    out = Path(sys.argv[1])
    src = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    raw = src.read_text(encoding="utf-8") if src else sys.stdin.read()
    obj = json.loads(raw)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(obj) if isinstance(obj, list) else "ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
