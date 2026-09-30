#!/usr/bin/env python3
"""Extract b64 field from MCP use_figma JSON (stdin or file) and write to path."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--file", type=Path, default=None)
    args = p.parse_args()
    raw = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
    data = json.loads(raw)
    b64 = data["b64"]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(b64, encoding="utf-8")
    print(json.dumps({"out": str(args.out), "count": data.get("count")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
