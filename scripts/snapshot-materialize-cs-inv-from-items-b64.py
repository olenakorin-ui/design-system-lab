#!/usr/bin/env python3
"""Decode cs-inv-part-{n}.itemsB64 MCP files into TSV slices and merged inventory."""
from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def decode_items(b64: str) -> list[dict]:
    raw = base64.b64decode(b64)
    return json.loads(raw.decode("utf-8"))


def items_to_tsv(items: list[dict]) -> str:
    lines = []
    for it in items:
        name = str(it["name"]).replace("\t", " ")
        page = it.get("page") or ""
        lines.append(f"{it['id']}\t{name}\t{page}")
    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--staging", type=Path, default=STAGING)
    p.add_argument("--write-tsv-slices", action="store_true", help="Also write cs-inv-{0..3}.tsv in 120-line chunks")
    args = p.parse_args()
    merged: list[dict] = []
    for path in sorted(args.staging.glob("cs-inv-part-*.mcp.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        b64 = data.get("itemsB64")
        if not b64:
            print(f"skip {path.name}: no itemsB64", file=sys.stderr)
            continue
        items = decode_items(b64)
        merged.extend(items)
        out = path.with_suffix(".json").with_name(path.name.replace(".mcp.json", ".json"))
        out.write_text(json.dumps({"items": items}, indent=2) + "\n", encoding="utf-8")
        print(path.name, len(items))
    if len(merged) != 405:
        print(f"total items {len(merged)} != 405", file=sys.stderr)
        return 2
    if args.write_tsv_slices:
        for i, start in enumerate((0, 120, 240, 360)):
            chunk = merged[start : start + 120]
            tsv_path = args.staging / f"cs-inv-{i}.tsv"
            tsv_path.write_text(items_to_tsv(chunk), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
