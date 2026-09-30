#!/usr/bin/env python3
"""Decode base64 JSON batch from stdin and write snapshot MCP artifact."""

from __future__ import annotations

import argparse
import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "design-system/snapshots/_raw/mcp"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--kind", required=True)
    p.add_argument("--batch", type=int, default=0)
    args = p.parse_args()
    payload = json.load(sys.stdin)
    raw = payload.get("b64") or payload.get("data")
    if not raw:
        raise SystemExit("missing b64")
    text = base64.b64decode(raw).decode("utf-8")
    data = json.loads(text)

    if args.kind == "index":
        out = MCP / f"component-sets-index.batch-{args.batch}.json"
    elif args.kind == "text":
        out = MCP / f"text-styles.batch-{args.batch}.json"
    elif args.kind == "effects":
        out = MCP / "effect-styles.json"
    elif args.kind == "known-badge":
        out = MCP / "component-sets-known.part-badge.json"
    elif args.kind == "known-checkbox":
        out = MCP / "component-sets-known.part-checkbox.json"
    elif args.kind.startswith("known-button"):
        out = MCP / f"component-sets-known.part-{args.kind.split('-', 1)[1]}.json"
    else:
        raise SystemExit(f"unknown kind {args.kind}")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n = len(data) if isinstance(data, list) else 1
    print(json.dumps({"path": str(out), "count": n}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
