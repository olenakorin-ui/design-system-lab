#!/usr/bin/env python3
"""Pull snapshot JSON from Figma plugin keys via use_figma (one key per invocation).

This script is invoked by the agent after each use_figma call writes a batch file:

  python3 scripts/sync-snapshot-from-figma-plugin.py ingest \\
    --kind index --batch 0 --stdin

Batch files land in design-system/snapshots/_raw/mcp/.

Then:

  python3 scripts/sync-snapshot-from-figma-plugin.py finalize
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "design-system/snapshots/_raw/mcp"


def ingest(kind: str, batch: int, data: object) -> None:
    if kind == "index":
        path = MCP / f"component-sets-index.batch-{batch}.json"
    elif kind == "text":
        path = MCP / f"text-styles.batch-{batch}.json"
    elif kind == "effects":
        path = MCP / "effect-styles.json"
    elif kind == "known-badge":
        path = MCP / "component-sets-known.part-badge.json"
    elif kind == "known-checkbox":
        path = MCP / "component-sets-known.part-checkbox.json"
    elif kind.startswith("known-button"):
        path = MCP / f"component-sets-known.part-{kind.split('-', 1)[1]}.json"
    else:
        raise SystemExit(f"unknown kind: {kind}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    n = len(data) if isinstance(data, list) else 1
    print(json.dumps({"written": str(path), "count": n}))


def finalize() -> None:
    import subprocess

    subprocess.run([sys.executable, str(ROOT / "scripts/materialize-snapshot-from-mcp.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/assemble-mcp-snapshot-raw.py")], check=True)


def main() -> int:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    ing = sub.add_parser("ingest")
    ing.add_argument("--kind", required=True)
    ing.add_argument("--batch", type=int, default=0)
    ing.add_argument("--stdin", action="store_true")
    sub.add_parser("finalize")
    args = p.parse_args()
    if args.cmd == "ingest":
        data = json.load(sys.stdin)
        ingest(args.kind, args.batch, data)
    else:
        finalize()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
