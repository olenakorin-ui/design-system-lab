#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    payload = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/snapshot-run-b64-fetch.py"), "ingest-slice"],
        input=json.dumps(payload).encode("utf-8"),
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
