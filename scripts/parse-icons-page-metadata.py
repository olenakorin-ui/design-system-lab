#!/usr/bin/env python3
"""Parse Figma get_metadata XML for Icons page symbols → icons.json shape."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SYMBOL_RE = re.compile(
    r'<symbol\s+id="([^"]+)"\s+name="([^"]+)"\s+x="[^"]+"\s+y="[^"]+"\s+width="[^"]+"\s+height="[^"]+"\s*/>'
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("metadata_xml", type=Path)
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=Path("design-system/snapshots/_raw/mcp/icons.json"),
    )
    args = parser.parse_args()
    text = args.metadata_xml.read_text(encoding="utf-8")
    icons = []
    for mid, name in SYMBOL_RE.findall(text):
        icons.append(
            {
                "id": mid,
                "name": name,
                "type": "COMPONENT",
                "page": "Icons",
                "description": "",
            }
        )
    icons.sort(key=lambda x: x["id"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(icons, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(icons), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
