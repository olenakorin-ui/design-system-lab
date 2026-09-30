#!/usr/bin/env python3
"""Reassemble base64 from ordered exp chunk ids and write decoded JSON to out path."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--fetch-json", required=True, help="JSON {order:[ids], chunks:{id:str}}")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    payload = json.loads(Path(args.fetch_json).read_text(encoding="utf-8"))
    order = payload["order"]
    chunks = payload["chunks"]
    b64 = "".join(chunks[i] for i in order)
    obj = json.loads(base64.b64decode(b64).decode("utf-8"))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(obj) if isinstance(obj, list) else "ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
