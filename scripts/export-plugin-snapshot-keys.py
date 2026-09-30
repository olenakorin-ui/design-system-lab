#!/usr/bin/env python3
"""Write MCP plugin-data export manifest and merge into snapshot files.

Expects batch JSON files written from Figma plugin keys:
  component-sets-index.batch-{0..4}.json  (from idx_*)
  text-styles.batch-{0..3}.json           (from txt_*)
  effect-styles.json                      (from effects)
  component-sets-known.part-{badge,checkbox,button0,button1,button2}.json
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MCP = ROOT / "design-system" / "snapshots" / "_raw" / "mcp"


def merge_known() -> None:
    parts: list[dict] = []
    for name in ("badge", "checkbox", "button0", "button1", "button2"):
        p = MCP / f"component-sets-known.part-{name}.json"
        if p.exists():
            parts.append(json.loads(p.read_text(encoding="utf-8")))

    by_id: dict[str, dict] = {}
    for part in parts:
        if not part or not part.get("id"):
            continue
        eid = part["id"]
        clean = {k: v for k, v in part.items() if k not in ("variantOffset", "variantTotal")}
        if eid not in by_id:
            by_id[eid] = clean
        else:
            by_id[eid]["variants"] = (by_id[eid].get("variants") or []) + (clean.get("variants") or [])

    out = {"componentSets": sorted(by_id.values(), key=lambda x: x["id"])}
    (MCP / "component-sets-known.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    subprocess.run([sys.executable, str(ROOT / "scripts" / "merge-snapshot-tsv-batches.py")], check=True)
    merge_known()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "assemble-mcp-snapshot-raw.py")], check=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
