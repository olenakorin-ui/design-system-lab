#!/usr/bin/env python3
"""Store one b64 slice from use_figma; assemble and ingest when all parts present."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--category", required=True)
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--part-index", type=int, required=True)
    p.add_argument("--total-parts", type=int, required=True)
    p.add_argument("--slice", default="")
    p.add_argument("--slice-file", type=Path, default=None)
    p.add_argument("--expected-b64-len", type=int, required=True)
    p.add_argument("--mcp-count", type=int, required=True)
    args = p.parse_args()
    STAGING.mkdir(parents=True, exist_ok=True)
    key = f"{args.category}-{args.index}"
    part_path = STAGING / f"{key}.part-{args.part_index:03d}.b64"
    slice_text = args.slice
    if args.slice_file:
        slice_text = args.slice_file.read_text(encoding="utf-8").strip()
    if not slice_text:
        print("missing slice", file=sys.stderr)
        return 2
    part_path.write_text(slice_text, encoding="utf-8")
    if args.part_index + 1 < args.total_parts:
        print(json.dumps({"status": "partial", "key": key, "part": args.part_index}))
        return 0
    b64 = "".join(
        (STAGING / f"{key}.part-{i:03d}.b64").read_text(encoding="utf-8")
        for i in range(args.total_parts)
    )
    if len(b64) != args.expected_b64_len:
        print(
            f"REJECTED: b64 len {len(b64)} != expected {args.expected_b64_len}",
            file=sys.stderr,
        )
        return 3
    b64_path = STAGING / f"{key}.b64"
    b64_path.write_text(b64, encoding="utf-8")
    proc = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/snapshot-ingest-b64.py"),
            "--category",
            args.category,
            "--index",
            str(args.index),
            "--requested",
            str(args.requested),
            "--b64-file",
            str(b64_path),
        ],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        print(proc.stderr or proc.stdout, file=sys.stderr)
        return proc.returncode
    meta = json.loads(proc.stdout)
    if meta.get("receivedCount") != args.mcp_count:
        print(
            f"WARN: mcp count {args.mcp_count} != ingested {meta.get('receivedCount')}",
            file=sys.stderr,
        )
    print(json.dumps({"status": "complete", "ingest": meta, "b64Len": len(b64)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
