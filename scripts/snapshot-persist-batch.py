#!/usr/bin/env python3
"""Persist a JSON items payload from stdin or --json into a snapshot batch."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

# load batch tools by path
import importlib.util
spec = importlib.util.spec_from_file_location("sbt", ROOT / "scripts" / "snapshot-batch-tools.py")
sbt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbt)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--category", required=True)
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--retry", type=int, default=0)
    p.add_argument("--file", type=Path, default=None)
    args = p.parse_args()
    if args.file:
        data = json.loads(args.file.read_text(encoding="utf-8"))
    else:
        data = json.loads(sys.stdin.read())
    items = data["items"] if isinstance(data, dict) and "items" in data else data
    meta = sbt.write_batch(
        args.category,
        args.index,
        items,
        requested_count=args.requested,
        retry_count=args.retry,
    )
    print(json.dumps(meta))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
