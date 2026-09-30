#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESP = ROOT / "design-system/snapshots/_raw/mcp/slice-responses"


def main() -> int:
    idx = int(sys.argv[1])
    data = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    RESP.mkdir(parents=True, exist_ok=True)
    out = RESP / f"cursor-{idx:02d}.json"
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
