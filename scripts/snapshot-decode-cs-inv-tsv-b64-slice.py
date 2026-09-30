#!/usr/bin/env python3
"""Decode cs-inv-s60-{start}.tsv from MCP JSON with tsvB64 field."""
from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def decode_tsv_b64(b64: str) -> str:
    return base64.b64decode(b64).decode("utf-8")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--mcp-json", type=Path, required=True)
    args = p.parse_args()
    data = json.loads(args.mcp_json.read_text(encoding="utf-8"))
    b64 = data.get("tsvB64")
    if not b64:
        raise SystemExit("missing tsvB64")
    tsv = decode_tsv_b64(b64)
    start = int(data["start"])
    STAGING.mkdir(parents=True, exist_ok=True)
    (STAGING / f"cs-inv-s60-{start}.tsv").write_text(tsv if tsv.endswith("\n") else tsv + "\n", encoding="utf-8")
    (STAGING / f"cs-inv-s60-{start}.mcp.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    n = len([ln for ln in tsv.splitlines() if ln.strip()])
    print(json.dumps({"start": start, "lines": n, "expected": data.get("count")}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
