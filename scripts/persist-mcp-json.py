#!/usr/bin/env python3
"""Write MCP JSON payload from stdin or a file path argument to an output path."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: persist-mcp-json.py <input.json> <output.json>", file=sys.stderr)
        return 2
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    obj = json.loads(src.read_text(encoding="utf-8"))
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if isinstance(obj, list):
        print(len(obj))
    elif isinstance(obj, dict):
        for key in ("items", "total", "componentSets"):
            if key in obj:
                print(f"{key}={obj[key] if key != 'items' else len(obj[key])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
