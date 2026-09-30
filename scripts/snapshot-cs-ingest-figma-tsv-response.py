#!/usr/bin/env python3
"""Ingest use_figma TSV / tsvChunks response into consecutive CS batches."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--start-index", type=int, required=True)
    p.add_argument("--lines-per-batch", type=int, default=8)
    p.add_argument("--response-file", type=Path, required=True)
    args = p.parse_args()
    data = json.loads(args.response_file.read_text(encoding="utf-8"))
    if "tsv" in data:
        tsv = data["tsv"]
    elif "tsvChunks" in data:
        tsv = "\n".join(data["tsvChunks"])
    else:
        print("ERROR: no tsv or tsvChunks", file=sys.stderr)
        return 2
    with tempfile.NamedTemporaryFile("w", suffix=".tsv", delete=False, encoding="utf-8") as tf:
        tf.write(tsv)
        tsv_path = Path(tf.name)
    cmd = [
        sys.executable,
        str(ROOT / "scripts" / "snapshot-cs-ingest-tsv-lines.py"),
        "--start-index",
        str(args.start_index),
        "--lines-per-batch",
        str(args.lines_per_batch),
        "--tsv-file",
        str(tsv_path),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        return r.returncode
    print(r.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
