#!/usr/bin/env python3
"""Append one b64 slice for a plugin key; decode when complete."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/mcp/b64-staging"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--key", required=True)
    p.add_argument("--part-index", type=int, required=True)
    p.add_argument("--total-parts", type=int, required=True)
    p.add_argument("--slice", required=True, help="b64 slice string")
    p.add_argument("--expected-len", type=int, default=0)
    args = p.parse_args()
    STAGING.mkdir(parents=True, exist_ok=True)
    part_path = STAGING / f"{args.key}.part-{args.part_index:03d}.b64"
    part_path.write_text(args.slice, encoding="utf-8")
    if args.part_index + 1 < args.total_parts:
        print(json.dumps({"status": "partial", "key": args.key, "part": args.part_index}))
        return 0
    parts = []
    for i in range(args.total_parts):
        pp = STAGING / f"{args.key}.part-{i:03d}.b64"
        if not pp.exists():
            raise SystemExit(f"missing part {pp}")
        parts.append(pp.read_text(encoding="utf-8"))
    b64 = "".join(parts)
    if args.expected_len and len(b64) != args.expected_len:
        raise SystemExit(f"len mismatch {args.key}: got {len(b64)} expected {args.expected_len}")
    full = STAGING / f"{args.key}.b64"
    full.write_text(b64, encoding="utf-8")
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/snapshot-plugin-key-to-batch.py"),
            "--key",
            args.key,
            "--b64-file",
            str(full),
        ],
        check=True,
    )
    print(json.dumps({"status": "complete", "key": args.key, "b64Len": len(b64)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
