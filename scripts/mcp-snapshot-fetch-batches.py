#!/usr/bin/env python3
"""Fetch Design System Snapshot v1 MCP raw batches via repeated use_figma-shaped extractions.

This script is invoked by the agent after loading figma-use; it writes batch files under
design-system/snapshots/_raw/mcp/ for merge by assemble-mcp-snapshot-raw.py.

It does NOT call Figma directly — batch payloads are passed as JSON files produced by MCP.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

MCP = Path(__file__).resolve().parents[1] / "design-system" / "snapshots" / "_raw" / "mcp"


def merge_index_parts() -> list[dict]:
    parts = sorted(MCP.glob("component-sets-index.part-*.json"))
    items: list[dict] = []
    for p in parts:
        items.extend(json.loads(p.read_text(encoding="utf-8")))
    items.sort(key=lambda x: str(x.get("id", "")))
    return items


def merge_text_batches() -> list[dict]:
    parts = sorted(MCP.glob("text-styles.batch-*.json"))
    items: list[dict] = []
    for p in parts:
        items.extend(json.loads(p.read_text(encoding="utf-8")))
    items.sort(key=lambda x: str(x.get("id", "")))
    return items


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] != "merge":
        print("usage: mcp-snapshot-fetch-batches.py merge", file=sys.stderr)
        return 2
    index = merge_index_parts()
    text = merge_text_batches()
    write = MCP / "component-sets-index.json"
    write.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    text_out = MCP / "text-styles.json"
    text_out.write_text(json.dumps(text, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"componentSetsIndex": len(index), "textStyles": len(text)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
