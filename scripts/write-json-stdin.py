#!/usr/bin/env python3
"""Read JSON from stdin and write pretty-printed to argv[1]."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: write-json-stdin.py <output.json>", file=sys.stderr)
        return 2
    obj = json.load(sys.stdin)
    path = Path(sys.argv[1])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if isinstance(obj, list):
        print(len(obj))
    elif isinstance(obj, dict):
        if "items" in obj and isinstance(obj["items"], list):
            print(len(obj["items"]))
        elif "componentSets" in obj:
            cs = obj["componentSets"]
            print(len(cs) if isinstance(cs, list) else 1)
        else:
            print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
