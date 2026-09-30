#!/usr/bin/env python3
"""Write exp-chunks/*.txt from use_figma fetch JSON {chunkId: b64Slice}."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / "design-system/snapshots/_raw/mcp/exp-chunks"


def main() -> int:
    payload = json.load(sys.stdin)
    CHUNKS.mkdir(parents=True, exist_ok=True)
    for cid, text in payload.items():
        (CHUNKS / f"{cid}.txt").write_text(text, encoding="utf-8")
    print(len(payload))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
