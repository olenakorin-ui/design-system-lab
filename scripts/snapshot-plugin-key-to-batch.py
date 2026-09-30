#!/usr/bin/env python3
"""Decode one plugin-key b64 file (stdin or --b64-file) into snapshot MCP batch path."""

from __future__ import annotations

import argparse
import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "design-system/snapshots/_raw/mcp"

INDEX = [f"idx_{i}" for i in range(5)]
TEXT = [f"txt_{i}" for i in range(4)]
KNOWN = {
    "known_badge": MCP / "component-sets-known.part-badge.json",
    "known_checkbox": MCP / "component-sets-known.part-checkbox.json",
    "known_button_0": MCP / "component-sets-known.part-button0.json",
    "known_button_1": MCP / "component-sets-known.part-button1.json",
    "known_button_2": MCP / "component-sets-known.part-button2.json",
}


def out_for_key(key: str) -> Path:
    if key in INDEX:
        return MCP / f"component-sets-index.batch-{INDEX.index(key)}.json"
    if key in TEXT:
        return MCP / f"text-styles.batch-{TEXT.index(key)}.json"
    if key == "effects":
        return MCP / "effect-styles.json"
    if key in KNOWN:
        return KNOWN[key]
    raise SystemExit(f"unknown key {key}")


def decode_b64(b64: str) -> object:
    text = base64.b64decode(b64.strip()).decode("utf-8")
    return json.loads(text)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--key", required=True)
    p.add_argument("--b64-file")
    args = p.parse_args()
    b64 = Path(args.b64_file).read_text(encoding="utf-8") if args.b64_file else __import__("sys").stdin.read()
    obj = decode_b64(b64)
    out = out_for_key(args.key)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"key": args.key, "path": str(out), "count": len(obj) if isinstance(obj, list) else 1}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
