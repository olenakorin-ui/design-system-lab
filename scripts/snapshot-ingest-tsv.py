#!/usr/bin/env python3
"""Ingest compact TSV detail batches from Figma MCP into snapshot batches.

Text TSV columns:
id, key, name, fontSize, fontFamily, fontStyle, lhUnit, lhValue,
lsUnit, lsValue, textCase, textDecoration, paragraphSpacing, paragraphIndent

Effect TSV is not used (JSON batches already complete).

Component-set TSV (index-level) columns:
id, key, name, page, variantCount, propKeys(|-joined)

Component-set DETAIL uses JSON b64 or NDJSON via other helpers.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sbt", ROOT / "scripts" / "snapshot-batch-tools.py")
sbt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbt)


def parse_num(v: str):
    if v == "" or v == "null":
        return None
    try:
        if "." in v:
            return float(v)
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v


def text_tsv_to_items(tsv: str) -> list[dict]:
    items = []
    for line in tsv.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 14:
            raise ValueError(f"text TSV expected 14 cols, got {len(parts)}: {line[:80]}")
        (
            sid,
            key,
            name,
            font_size,
            family,
            style,
            lh_unit,
            lh_value,
            ls_unit,
            ls_value,
            text_case,
            text_decoration,
            para_spacing,
            para_indent,
        ) = parts[:14]
        lh: dict
        if lh_unit == "AUTO" or lh_value in ("", "null", None):
            lh = {"unit": "AUTO"}
        else:
            lh = {"unit": lh_unit, "value": parse_num(lh_value)}
        ls = {"unit": ls_unit, "value": parse_num(ls_value) if ls_value not in ("", "null") else 0}
        items.append(
            {
                "id": sid,
                "key": key or None,
                "name": name,
                "description": "",
                "styleType": "TEXT",
                "details": {
                    "fontSize": parse_num(font_size),
                    "fontName": {"family": family, "style": style},
                    "lineHeight": lh,
                    "letterSpacing": ls,
                    "textCase": text_case,
                    "textDecoration": text_decoration,
                    "paragraphSpacing": parse_num(para_spacing) or 0,
                    "paragraphIndent": parse_num(para_indent) or 0,
                },
            }
        )
    return items


def component_tsv_to_items(tsv: str) -> list[dict]:
    """Minimal inventory-style component rows → full-enough snapshot rows (no set)."""
    items = []
    for line in tsv.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 4:
            raise ValueError(f"component TSV expected >=4 cols, got {len(parts)}")
        sid, key, name, page = parts[:4]
        desc = parts[4] if len(parts) > 4 else ""
        items.append(
            {
                "id": sid,
                "key": key or None,
                "name": name,
                "description": desc,
                "page": page,
                "componentSetId": None,
                "componentPropertyDefinitions": {},
            }
        )
    return items


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--category", required=True, choices=("text-styles", "components"))
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--retry", type=int, default=0)
    p.add_argument("--tsv-file", type=Path, required=True)
    args = p.parse_args()
    tsv = args.tsv_file.read_text(encoding="utf-8")
    # allow wrapper JSON {"tsv":"..."}
    if tsv.lstrip().startswith("{"):
        tsv = json.loads(tsv)["tsv"]
    try:
        if args.category == "text-styles":
            items = text_tsv_to_items(tsv)
        else:
            items = component_tsv_to_items(tsv)
    except ValueError as e:
        sbt.mark_truncation(args.category, args.index, reduced=False)
        print(f"REJECTED: {e}", file=sys.stderr)
        return 3
    ok, reason = sbt.validate_batch_payload(args.category, items, requested_count=args.requested)
    if not ok:
        sbt.mark_truncation(args.category, args.index, reduced=False)
        print(f"REJECTED: {reason}", file=sys.stderr)
        return 3
    meta = sbt.write_batch(
        args.category,
        args.index,
        items,
        requested_count=args.requested,
        retry_count=args.retry,
    )
    print(json.dumps(meta))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
