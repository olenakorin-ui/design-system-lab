#!/usr/bin/env python3
"""Decode UTF-8 JSON from Figma plugin b64 (btoa/unescape/encodeURIComponent) on stdin."""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path


def decode_b64_json(b64: str) -> object:
    raw = base64.b64decode(b64.strip()).decode("utf-8")
    return json.loads(raw)


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: decode-plugin-b64.py <out.json> [--stdin-b64]", file=sys.stderr)
        return 2
    out = Path(sys.argv[1])
    b64 = sys.stdin.read()
    obj = decode_b64_json(b64)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(obj) if isinstance(obj, list) else "ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
