#!/usr/bin/env python3
"""Ingest compact component-set TSV detail lines into snapshot batches.

Columns:
id, key, name, page, defaultVariantId, propsJson, variantsSemi
where variantsSemi = id|key|name;id|key|name;...
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


def parse_tsv(tsv: str) -> list[dict]:
    items = []
    for line in tsv.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 7:
            raise ValueError(f"expected 7 cols, got {len(parts)}: {line[:100]}")
        sid, key, name, page, default_vid, props_json, vars_semi = parts[:7]
        defs = json.loads(props_json) if props_json else {}
        variants = []
        if vars_semi:
            for chunk in vars_semi.split(";"):
                if not chunk:
                    continue
                vp = chunk.split("|")
                if len(vp) < 3:
                    raise ValueError(f"bad variant chunk: {chunk}")
                variants.append(
                    {
                        "id": vp[0],
                        "key": vp[1] or None,
                        "name": vp[2],
                        "description": "",
                        "componentProperties": {},
                    }
                )
        items.append(
            {
                "id": sid,
                "key": key or None,
                "name": name,
                "description": "",
                "page": page or None,
                "componentPropertyDefinitions": defs,
                "defaultVariantId": default_vid or None,
                "variants": variants,
            }
        )
    return items


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--retry", type=int, default=0)
    p.add_argument("--tsv-file", type=Path, required=True)
    args = p.parse_args()
    raw = args.tsv_file.read_text(encoding="utf-8")
    if raw.lstrip().startswith("{"):
        raw = json.loads(raw)["tsv"]
    try:
        items = parse_tsv(raw)
    except (ValueError, json.JSONDecodeError) as e:
        sbt.mark_truncation("component-sets", args.index, reduced=False)
        print(f"REJECTED: {e}", file=sys.stderr)
        return 3
    ok, reason = sbt.validate_batch_payload("component-sets", items, requested_count=args.requested)
    if not ok:
        sbt.mark_truncation("component-sets", args.index, reduced=False)
        print(f"REJECTED: {reason}", file=sys.stderr)
        return 3
    meta = sbt.write_batch(
        "component-sets",
        args.index,
        items,
        requested_count=args.requested,
        retry_count=args.retry,
    )
    print(json.dumps(meta))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
