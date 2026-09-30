#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BATCHES = ROOT / "design-system/snapshots/_raw/mcp/b64-job-batches.json"


def main() -> int:
    idx = int(sys.argv[1])
    batches = json.loads(BATCHES.read_text(encoding="utf-8"))
    jobs = batches[idx]
    print(
        f"""const NS = 'ds.snapshot.v1';
const jobs = {json.dumps(jobs)};
return jobs.map((j) => {{
  const b64 = figma.root.getSharedPluginData(NS, 'b64_' + j.key) ?? '';
  const start = j.partIndex * j.size;
  return {{
    key: j.key,
    expectedLen: b64.length,
    partIndex: j.partIndex,
    totalParts: j.totalParts,
    slice: b64.slice(start, start + j.size),
  }};
}});"""
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
