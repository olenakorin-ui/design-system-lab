#!/usr/bin/env python3
"""Reassemble snapshot JSON written to Figma hidden text nodes (chunk files)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "design-system" / "snapshots" / "_raw" / "mcp"
CHUNK_DIR = MCP / "chunks"


def reassemble(prefix: str, out_name: str) -> int:
    parts: list[str] = []
    for p in sorted(CHUNK_DIR.glob(f"{prefix}.part-*")):
        parts.append(p.read_text(encoding="utf-8"))
    text = "".join(parts)
    obj = json.loads(text)
    out = MCP / out_name
    out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(obj) if isinstance(obj, list) else len(obj.get("componentSets", []))


def main() -> int:
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    counts = {
        "component-sets-index.json": reassemble("index", "component-sets-index.json"),
        "text-styles.json": reassemble("text", "text-styles.json"),
        "effect-styles.json": reassemble("effects", "effect-styles.json"),
        "component-sets-known.json": reassemble("known", "component-sets-known.json"),
    }
    print(json.dumps(counts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
