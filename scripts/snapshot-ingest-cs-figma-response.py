#!/usr/bin/env python3
"""Ingest use_figma component-set pack response (items, b64, or TSV) into snapshot batch."""
from __future__ import annotations

import argparse
import base64
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging"


def reassemble_chunks(chunks: list[str]) -> str:
    return "".join(chunks)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--index", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--response-file", type=Path, required=True)
    p.add_argument("--retry", type=int, default=0)
    args = p.parse_args()
    data = json.loads(args.response_file.read_text(encoding="utf-8"))

    if "items" in data:
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
            json.dump({"items": data["items"]}, tf)
            items_file = Path(tf.name)
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "snapshot-cs-ingest-items.py"),
            "--index",
            str(args.index),
            "--requested",
            str(args.requested),
            "--items-file",
            str(items_file),
        ]
    elif "tsv" in data or "tsvChunks" in data:
        tsv = data.get("tsv") or reassemble_chunks(data["tsvChunks"])
        tsv_path = STAGING / f"cs-response-{args.index:04d}.tsv"
        tsv_path.parent.mkdir(parents=True, exist_ok=True)
        tsv_path.write_text(tsv, encoding="utf-8")
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "snapshot-ingest-cs-tsv.py"),
            "--index",
            str(args.index),
            "--requested",
            str(args.requested),
            "--retry",
            str(args.retry),
            "--tsv-file",
            str(tsv_path),
        ]
    elif "b64" in data or "b64Chunks" in data:
        b64 = data.get("b64") or reassemble_chunks(data["b64Chunks"])
        b64_path = STAGING / f"cs-response-{args.index:04d}.b64"
        b64_path.parent.mkdir(parents=True, exist_ok=True)
        b64_path.write_text(b64, encoding="utf-8")
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "snapshot-ingest-b64.py"),
            "--category",
            "component-sets",
            "--index",
            str(args.index),
            "--requested",
            str(args.requested),
            "--retry",
            str(args.retry),
            "--b64-file",
            str(b64_path),
        ]
    else:
        print("ERROR: response missing items, b64, or tsv", file=sys.stderr)
        return 2

    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        print(r.stdout)
        return r.returncode
    print(r.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
