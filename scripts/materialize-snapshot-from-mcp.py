#!/usr/bin/env python3
"""Write snapshot MCP artifacts from JSON batch files (stdin or paths)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "design-system/snapshots/_raw/mcp"


def write_list(path: Path, items: list) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(items)


def merge_index_batches() -> int:
    items: list = []
    for p in sorted(MCP.glob("component-sets-index.batch-*.json")):
        items.extend(json.loads(p.read_text(encoding="utf-8")))
    by_id = {x["id"]: x for x in items}
    return write_list(MCP / "component-sets-index.json", sorted(by_id.values(), key=lambda x: x["id"]))


def merge_text_batches() -> int:
    items: list = []
    for p in sorted(MCP.glob("text-styles.batch-*.json")):
        items.extend(json.loads(p.read_text(encoding="utf-8")))
    by_id = {x["id"]: x for x in items}
    return write_list(MCP / "text-styles.json", sorted(by_id.values(), key=lambda x: x["id"]))


def merge_known() -> int:
    badge = json.loads((MCP / "component-sets-known.part-badge.json").read_text(encoding="utf-8"))
    checkbox = json.loads((MCP / "component-sets-known.part-checkbox.json").read_text(encoding="utf-8"))
    button_parts = []
    for p in sorted(MCP.glob("component-sets-known.part-button*.json")):
        button_parts.append(json.loads(p.read_text(encoding="utf-8")))
    button = button_parts[0] if button_parts else None
    if button:
        variants = []
        for part in button_parts:
            variants.extend(part.get("variants") or [])
        button = {k: v for k, v in button.items() if k not in ("variantOffset", "variantTotal")}
        button["variants"] = variants
    out = {"componentSets": [badge, checkbox, button]}
    out["componentSets"] = [s for s in out["componentSets"] if s]
    path = MCP / "component-sets-known.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(out["componentSets"])


def main() -> int:
    counts = {
        "index": merge_index_batches(),
        "text": merge_text_batches(),
        "known": merge_known() if (MCP / "component-sets-known.part-badge.json").exists() else 0,
    }
    print(json.dumps(counts))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
