#!/usr/bin/env python3
"""Merge MCP batch files into snapshot raw artifacts + figma-export.latest.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "design-system" / "snapshots" / "_raw" / "mcp"
RAW = ROOT / "design-system" / "snapshots" / "_raw" / "figma-export.latest.json"
KNOWN_NAMES = {"Button", "Badge", "Checkbox"}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def merge_batches(glob: str) -> list[Any]:
    items: list[Any] = []
    for p in sorted(MCP.glob(glob)):
        data = load_json(p)
        if isinstance(data, list):
            items.extend(data)
        elif isinstance(data, dict) and "items" in data:
            items.extend(data["items"])
    return items


def stub_from_index(entry: dict) -> dict:
    return {
        "id": entry["id"],
        "key": entry.get("key"),
        "name": entry["name"],
        "page": entry.get("page", ""),
        "componentPropertyDefinitions": {},
        "defaultVariantId": None,
        "variants": [],
    }


def main() -> int:
    vars_live = load_json(MCP / "variables-from-live.json")

    text = merge_batches("text-styles.batch-*.json")
    text = sorted(text, key=lambda x: str(x.get("id", "")))

    effects = load_json(MCP / "effect-styles.json") if (MCP / "effect-styles.json").exists() else []

    icons = merge_batches("icons.batch-*.json")
    if not icons and (MCP / "icons.json").exists():
        icons = load_json(MCP / "icons.json")
        if isinstance(icons, dict) and "icons" in icons:
            icons = icons["icons"]
    icons = sorted(icons, key=lambda x: str(x.get("id", "")))

    index = load_json(MCP / "component-sets-index.json") if (MCP / "component-sets-index.json").exists() else []

    known_path = MCP / "component-sets-known.json"
    known_sets: list[dict] = []
    if known_path.exists():
        known_data = load_json(known_path)
        known_sets = known_data.get("componentSets") or known_data
        if isinstance(known_sets, dict):
            known_sets = known_sets.get("componentSets", [])

    known_by_id = {s["id"]: s for s in known_sets if isinstance(s, dict) and s.get("id")}

    component_sets: list[dict] = []
    for entry in sorted(index, key=lambda x: str(x.get("id", ""))):
        eid = entry["id"]
        if eid in known_by_id:
            component_sets.append(known_by_id[eid])
        else:
            component_sets.append(stub_from_index(entry))

    # Ensure known sets present even if missing from index
    for s in known_sets:
        if s.get("id") and not any(c.get("id") == s["id"] for c in component_sets):
            component_sets.append(s)
    component_sets = sorted(component_sets, key=lambda x: str(x.get("id", "")))

    write_json(MCP / "text-styles.json", text)
    if not (MCP / "effect-styles.json").exists() and effects:
        write_json(MCP / "effect-styles.json", effects)
    write_json(MCP / "icons.json", icons)

    export = {
        "file": vars_live.get("file") or {"key": "ZllxQplWi5QJcNeUHeY8T3", "name": "Design System V2"},
        "sourceCapabilities": {
            "variables": "complete",
            "components": "partial",
            "styles": "partial",
            "icons": "partial",
            "previews": "deferred",
            "structuralAudit": "deferred",
        },
        "collections": vars_live.get("collections") or [],
        "variables": vars_live.get("variables") or [],
        "componentSets": component_sets,
        "components": [],
        "styles": {
            "text": text,
            "effect": effects if isinstance(effects, list) else [],
            "paint": [],
            "grid": [],
        },
        "icons": {
            "page": {"id": "1:433", "name": "Icons"},
            "icons": icons,
        },
    }
    write_json(RAW, export)

    print(
        json.dumps(
            {
                "textStyles": len(text),
                "effectStyles": len(effects) if isinstance(effects, list) else 0,
                "icons": len(icons),
                "componentSetsIndex": len(index),
                "componentSetsKnown": len(known_sets),
                "componentSetsExport": len(component_sets),
                "variables": len(export["variables"]),
                "collections": len(export["collections"]),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
