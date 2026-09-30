#!/usr/bin/env python3
"""Write one Figma snapshot text slice to mcp/chunks/{prefix}.part-{n:03d}."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNK_DIR = ROOT / "design-system/snapshots/_raw/mcp/chunks"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--prefix", required=True)
    p.add_argument("--part", type=int, required=True)
    args = p.parse_args()
    text = sys.stdin.read()
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    out = CHUNK_DIR / f"{args.prefix}.part-{args.part:03d}"
    out.write_text(text, encoding="utf-8")
    print(len(text))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
