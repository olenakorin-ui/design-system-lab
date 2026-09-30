#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--kind", required=True)
    p.add_argument("--batch", type=int, default=0)
    p.add_argument("--file", required=True)
    args = p.parse_args()
    data = json.loads(Path(args.file).read_text(encoding="utf-8"))
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/sync-snapshot-from-figma-plugin.py"),
            "ingest",
            "--kind",
            args.kind,
            "--batch",
            str(args.batch),
            "--stdin",
        ],
        input=json.dumps(data).encode("utf-8"),
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
