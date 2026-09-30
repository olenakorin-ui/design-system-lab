#!/usr/bin/env python3
"""Ingest all fetch_cursor_* slice batches saved under mcp/slice-responses/."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESP = ROOT / "design-system/snapshots/_raw/mcp/slice-responses"
INGEST = ROOT / "scripts/snapshot-ingest-slice-batch.py"


def main() -> int:
    paths = sorted(RESP.glob("cursor-*.json"))
    if not paths:
        print("no slice-responses/cursor-*.json files", file=sys.stderr)
        return 2
    for p in paths:
        subprocess.run([sys.executable, str(INGEST), str(p)], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/materialize-snapshot-from-mcp.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/assemble-mcp-snapshot-raw.py")], check=True)
    print(json.dumps({"ingestedFiles": len(paths)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
