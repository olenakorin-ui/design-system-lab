#!/usr/bin/env python3
"""Materialize snapshot MCP files from base64 staging lines (one file per plugin key).

Staging layout: design-system/snapshots/_raw/mcp/b64-staging/<plugin_key>.b64
Plugin keys: idx_0..4, txt_0..3, effects, known_badge, known_checkbox, known_button_0..2
"""

from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "design-system/snapshots/_raw/mcp"
STAGING = MCP / "b64-staging"

INDEX_KEYS = [f"idx_{i}" for i in range(5)]
TEXT_KEYS = [f"txt_{i}" for i in range(4)]
KNOWN_KEYS = [
    "known_badge",
    "known_checkbox",
    "known_button_0",
    "known_button_1",
    "known_button_2",
]


def decode_key(key: str) -> object:
    path = STAGING / f"{key}.b64"
    if not path.exists():
        raise FileNotFoundError(path)
    raw = base64.b64decode(path.read_text(encoding="utf-8").strip()).decode("utf-8")
    return json.loads(raw)


def write(path: Path, obj: object) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return len(obj) if isinstance(obj, list) else 1


def main() -> int:
    counts: dict[str, int] = {}
    for i, key in enumerate(INDEX_KEYS):
        p = STAGING / f"{key}.b64"
        if p.exists():
            data = decode_key(key)
            counts[key] = write(MCP / f"component-sets-index.batch-{i}.json", data)
    for i, key in enumerate(TEXT_KEYS):
        p = STAGING / f"{key}.b64"
        if p.exists():
            data = decode_key(key)
            counts[key] = write(MCP / f"text-styles.batch-{i}.json", data)
    if (STAGING / "effects.b64").exists():
        counts["effects"] = write(MCP / "effect-styles.json", decode_key("effects"))
    known_map = {
        "known_badge": MCP / "component-sets-known.part-badge.json",
        "known_checkbox": MCP / "component-sets-known.part-checkbox.json",
        "known_button_0": MCP / "component-sets-known.part-button0.json",
        "known_button_1": MCP / "component-sets-known.part-button1.json",
        "known_button_2": MCP / "component-sets-known.part-button2.json",
    }
    for key, out in known_map.items():
        p = STAGING / f"{key}.b64"
        if p.exists():
            counts[key] = write(out, decode_key(key))
    print(json.dumps(counts, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
