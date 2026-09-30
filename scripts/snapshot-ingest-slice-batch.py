#!/usr/bin/env python3
"""Ingest an array of b64 slice payloads from use_figma."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    items = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    if isinstance(items, dict) and "slice" in items:
        items = [items]
    for payload in items:
        subprocess.run(
            [sys.executable, str(ROOT / "scripts/snapshot-run-b64-fetch.py"), "ingest-slice"],
            input=json.dumps(payload).encode("utf-8"),
            check=True,
        )
    print(len(items))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
