#!/usr/bin/env python3
"""Read MCP JSON from stdin and run snapshot-persist-mcp-b64-batch."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if len(sys.argv) < 4:
        print("usage: snapshot-ingest-mcp-stdin.py CATEGORY INDEX REQUESTED", file=sys.stderr)
        return 2
    category, index, requested = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    data = json.load(sys.stdin)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
        json.dump(data, f)
        path = Path(f.name)
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/snapshot-persist-mcp-b64-batch.py"),
            "--category",
            category,
            "--index",
            str(index),
            "--requested",
            str(requested),
            "--response-file",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    path.unlink(missing_ok=True)
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return proc.returncode
    print(proc.stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
