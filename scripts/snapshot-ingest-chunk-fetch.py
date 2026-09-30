#!/usr/bin/env python3
"""Write exp-chunks/*.txt from a use_figma return object {chunkId: slice}."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHUNKS = ROOT / "design-system/snapshots/_raw/mcp/exp-chunks"


def main() -> int:
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    CHUNKS.mkdir(parents=True, exist_ok=True)
    n = 0
    for cid, text in payload.items():
        if not cid.startswith("exp_"):
            continue
        (CHUNKS / f"{cid}.txt").write_text(text or "", encoding="utf-8")
        n += 1
    print(n)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
