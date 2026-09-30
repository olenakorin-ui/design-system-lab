#!/usr/bin/env python3
"""Decode a base64 JSON array (or {items:[...]}) and write a validated snapshot batch."""
from __future__ import annotations
import argparse, base64, json, sys
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("sbt", ROOT / "scripts" / "snapshot-batch-tools.py")
sbt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sbt)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--category", required=True)
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--retry", type=int, default=0)
    p.add_argument("--b64-file", type=Path, required=True)
    args = p.parse_args()
    raw = args.b64_file.read_text(encoding="utf-8").strip()
    # allow wrapping JSON {"b64":"..."} or bare b64
    if raw.startswith("{"):
        raw = json.loads(raw)["b64"]
    data = json.loads(base64.b64decode(raw).decode("utf-8"))
    items = data["items"] if isinstance(data, dict) and "items" in data else data
    if not isinstance(items, list):
        print("ERROR: expected list", file=sys.stderr)
        return 2
    # structural completeness check
    ok, reason = sbt.validate_batch_payload(args.category, items, requested_count=args.requested)
    if not ok:
        sbt.mark_truncation(args.category, args.index, reduced=False)
        print(f"REJECTED: {reason}", file=sys.stderr)
        return 3
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
