#!/usr/bin/env python3
"""Write cs-inv-s60-{start}.tsv.b64 from --b64-file or --b64 literal."""
from __future__ import annotations

import argparse
from pathlib import Path

ST = Path(__file__).resolve().parents[1] / "design-system/snapshots/_raw/batches/inventories/_staging"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--start", type=int, required=True)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--b64", type=str)
    g.add_argument("--b64-file", type=Path)
    args = p.parse_args()
    b64 = args.b64 if args.b64 is not None else args.b64_file.read_text(encoding="utf-8").strip()
    ST.mkdir(parents=True, exist_ok=True)
    out = ST / f"cs-inv-s60-{args.start}.tsv.b64"
    out.write_text(b64.strip() + "\n", encoding="utf-8")
    print(out, len(b64))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
