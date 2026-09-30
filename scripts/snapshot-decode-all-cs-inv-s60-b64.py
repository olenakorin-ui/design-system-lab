#!/usr/bin/env python3
"""Decode cs-inv-s60-{start}.tsv.b64 files to .tsv."""
from __future__ import annotations

import base64
import json
from pathlib import Path

ST = Path(__file__).resolve().parents[1] / "design-system/snapshots/_raw/batches/inventories/_staging"


def main() -> int:
    total = 0
    for b64_path in sorted(ST.glob("cs-inv-s60-*.tsv.b64")):
        start = int(b64_path.name.replace("cs-inv-s60-", "").replace(".tsv.b64", ""))
        b64 = b64_path.read_text(encoding="utf-8").strip()
        tsv = base64.b64decode(b64).decode("utf-8")
        out = ST / f"cs-inv-s60-{start}.tsv"
        out.write_text(tsv if tsv.endswith("\n") else tsv + "\n", encoding="utf-8")
        n = len([ln for ln in tsv.splitlines() if ln.strip()])
        total += n
        print(start, n)
    print("total", total)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
