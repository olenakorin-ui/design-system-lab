#!/usr/bin/env python3
"""Write cs-inv-s60-{start}.tsv.b64 from JSON map start -> {tsvB64, count}."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WRITE = ROOT / "scripts/snapshot-write-cs-inv-tsv-b64.py"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("slices_json", type=Path)
    args = p.parse_args()
    data = json.loads(args.slices_json.read_text(encoding="utf-8"))
    for start_s, payload in sorted(data.items(), key=lambda x: int(x[0])):
        start = int(start_s)
        b64 = payload["tsvB64"].strip()
        subprocess.run(
            [sys.executable, str(WRITE), "--start", str(start), "--b64", b64],
            check=True,
            cwd=ROOT,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
