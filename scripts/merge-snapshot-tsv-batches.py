#!/usr/bin/env python3
"""Merge MCP batch JSON files into snapshot _raw/mcp artifacts."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "design-system" / "snapshots" / "_raw" / "mcp"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def merge_glob(pattern: str) -> list[Any]:
    out: list[Any] = []
    for p in sorted(MCP.glob(pattern)):
        data = load_json(p)
        if isinstance(data, list):
            out.extend(data)
        elif isinstance(data, dict) and "items" in data:
            out.extend(data["items"])
    return out


def main() -> int:
    index = merge_glob("component-sets-index.batch-*.json")
    index = sorted({e["id"]: e for e in index if e.get("id")}.values(), key=lambda x: x["id"])
    write_json(MCP / "component-sets-index.json", index)

    text = merge_glob("text-styles.batch-*.json")
    text = sorted({e["id"]: e for e in text if e.get("id")}.values(), key=lambda x: x["id"])
    write_json(MCP / "text-styles.json", text)

    known_parts = merge_glob("component-sets-known.part-*.json")
    if known_parts:
        by_id: dict[str, dict] = {}
        for part in known_parts:
            for s in part if isinstance(part, list) else [part]:
                if not isinstance(s, dict) or not s.get("id"):
                    continue
                eid = s["id"]
                if eid not in by_id:
                    by_id[eid] = s
                else:
                    existing = by_id[eid]
                    existing.setdefault("variants", []).extend(s.get("variants") or [])
        known = {"componentSets": sorted(by_id.values(), key=lambda x: x["id"])}
        write_json(MCP / "component-sets-known.json", known)

    print(
        json.dumps(
            {
                "componentSetsIndex": len(index),
                "textStyles": len(text),
                "knownParts": len(known_parts),
            }
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
