#!/usr/bin/env python3
"""Decode {order, chunks} fetch payload (b64 concat) to JSON and write out path."""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fetch-json", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    payload = json.loads(Path(args.fetch_json).read_text(encoding="utf-8"))
    b64 = "".join(payload["chunks"][i] for i in payload["order"])
    obj = json.loads(base64.b64decode(b64).decode("utf-8"))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(obj) if isinstance(obj, list) else "ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
