#!/usr/bin/env python3
"""Ingest component-set TSV into consecutive snapshot batches (split by line count)."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
import importlib.util

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("cs_tsv", ROOT / "scripts" / "snapshot-ingest-cs-tsv.py")
cs_tsv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs_tsv)
spec2 = importlib.util.spec_from_file_location("sbt", ROOT / "scripts" / "snapshot-batch-tools.py")
sbt = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(sbt)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--start-index", type=int, required=True)
    p.add_argument("--lines-per-batch", type=int, default=8)
    p.add_argument("--tsv-file", type=Path, required=True)
    args = p.parse_args()
    raw = args.tsv_file.read_text(encoding="utf-8")
    if raw.lstrip().startswith("{"):
        raw = json.loads(raw)["tsv"]
    lines = [ln for ln in raw.strip().splitlines() if ln.strip()]
    metas = []
    idx = args.start_index
    for i in range(0, len(lines), args.lines_per_batch):
        chunk = "\n".join(lines[i : i + args.lines_per_batch])
        items = cs_tsv.parse_tsv(chunk)
        ok, reason = sbt.validate_batch_payload("component-sets", items, requested_count=len(items))
        if not ok:
            sbt.mark_truncation("component-sets", idx, reduced=False)
            print(f"REJECTED batch {idx}: {reason}", file=sys.stderr)
            return 3
        meta = sbt.write_batch(
            "component-sets",
            idx,
            items,
            requested_count=len(items),
        )
        metas.append(meta)
        idx += 1
    print(json.dumps({"batches": metas, "totalLines": len(lines)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
