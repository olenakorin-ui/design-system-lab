#!/usr/bin/env python3
"""Fetch one ds.snapshot.v1 plugin JSON string key and write parsed JSON to out path."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--plugin-key", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()
    # This script is invoked after the agent saves raw plugin JSON to stdin.
    obj = json.load(sys.stdin)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(obj) if isinstance(obj, list) else "ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
