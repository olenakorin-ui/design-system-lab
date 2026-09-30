#!/usr/bin/env python3
"""Decode ds.snapshot.v1 exp_* chunks (already on Figma root) from local chunk files."""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "design-system/snapshots/_raw/mcp"
CHUNKS = MCP / "exp-chunks"
MANIFEST = MCP / "exp-manifest.json"

INDEX_KEYS = [f"idx_{i}" for i in range(5)]
TEXT_KEYS = [f"txt_{i}" for i in range(4)]
KNOWN_MAP = {
    "known_badge": MCP / "component-sets-known.part-badge.json",
    "known_checkbox": MCP / "component-sets-known.part-checkbox.json",
    "known_button_0": MCP / "component-sets-known.part-button0.json",
    "known_button_1": MCP / "component-sets-known.part-button1.json",
    "known_button_2": MCP / "component-sets-known.part-button2.json",
}


def out_path(plugin_key: str) -> Path:
    if plugin_key in INDEX_KEYS:
        return MCP / f"component-sets-index.batch-{INDEX_KEYS.index(plugin_key)}.json"
    if plugin_key in TEXT_KEYS:
        return MCP / f"text-styles.batch-{TEXT_KEYS.index(plugin_key)}.json"
    if plugin_key == "effects":
        return MCP / "effect-styles.json"
    if plugin_key in KNOWN_MAP:
        return KNOWN_MAP[plugin_key]
    raise KeyError(plugin_key)


def decode_entry(entry: dict) -> object:
    parts = entry["parts"]
    b64 = ""
    for part in parts:
        cid = part["id"]
        chunk_path = CHUNKS / f"{cid}.txt"
        if not chunk_path.exists():
            raise FileNotFoundError(chunk_path)
        b64 += chunk_path.read_text(encoding="utf-8")
    return json.loads(base64.b64decode(b64).decode("utf-8"))


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--manifest", default=str(MANIFEST))
    args = p.parse_args()
    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    counts: dict[str, int] = {}
    for section in ("index", "text", "effects", "known"):
        for entry in manifest.get(section, []):
            key = entry["pluginKey"]
            obj = decode_entry(entry)
            out = out_path(key)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            counts[key] = len(obj) if isinstance(obj, list) else 1
    print(json.dumps(counts, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
