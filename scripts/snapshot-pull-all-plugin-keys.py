#!/usr/bin/env python3
"""Materialize all snapshot batches from b64-staging/*.b64 (from use_figma btoa export).

Expected staging files (from sequential use_figma calls):
  idx_0..4, txt_0..3, effects, known_badge, known_checkbox,
  known_button_0..2 (full b64 or part files merged as known_button_N.b64)
"""

from __future__ import annotations

import base64
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/mcp/b64-staging"
MCP = ROOT / "design-system/snapshots/_raw/mcp"
KEYS = (
    [f"idx_{i}" for i in range(5)]
    + [f"txt_{i}" for i in range(4)]
    + ["effects", "known_badge", "known_checkbox", "known_button_0", "known_button_1", "known_button_2"]
)


def decode_key(key: str) -> object:
    path = STAGING / f"{key}.b64"
    if not path.exists():
        part_paths = sorted(STAGING.glob(f"{key}.part-*.b64"))
        if not part_paths:
            raise FileNotFoundError(path)
        b64 = "".join(p.read_text(encoding="utf-8").strip() for p in part_paths)
    else:
        b64 = path.read_text(encoding="utf-8").strip()
    return json.loads(base64.b64decode(b64).decode("utf-8"))


def main() -> int:
    counts: dict[str, int] = {}
    for key in KEYS:
        p = STAGING / f"{key}.b64"
        parts = list(STAGING.glob(f"{key}.part-*.b64"))
        if not p.exists() and not parts:
            continue
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "scripts/snapshot-plugin-key-to-batch.py"),
                "--key",
                key,
                "--b64-file",
                str(p if p.exists() else parts[0]),
            ],
            check=True,
        )
    subprocess.run([sys.executable, str(ROOT / "scripts/materialize-snapshot-from-mcp.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/assemble-mcp-snapshot-raw.py")], check=True)
    print("done")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
