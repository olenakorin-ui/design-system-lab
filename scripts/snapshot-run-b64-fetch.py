#!/usr/bin/env python3
"""Orchestrate b64 plugin-key export via use_figma (agent-driven).

Prints the next fetch job as JSON until all keys complete, then runs materialize + assemble.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "scripts/snapshot-b64-fetch-plan.json"
STATE = ROOT / "design-system/snapshots/_raw/mcp/b64-fetch-state.json"
INGEST = ROOT / "scripts/snapshot-ingest-b64-slice.py"


def load_plan() -> list[dict]:
    return json.loads(PLAN.read_text(encoding="utf-8"))


def load_state() -> dict:
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"done": [], "pending": {}}


def save_state(state: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")


def js_for(key: str, part_index: int, size: int) -> str:
    return f"""const NS = 'ds.snapshot.v1';
const key = {json.dumps(key)};
const size = {size};
const partIndex = {part_index};
const b64 = figma.root.getSharedPluginData(NS, 'b64_' + key) ?? '';
const totalParts = Math.ceil(b64.length / size) || 1;
const start = partIndex * size;
return {{
  key,
  expectedLen: b64.length,
  partIndex,
  totalParts,
  slice: b64.slice(start, start + size),
}};"""


def next_job() -> dict | None:
    plan = load_plan()
    state = load_state()
    done = set(state.get("done") or [])
    for entry in plan:
        key = entry["key"]
        if key in done:
            continue
        size = entry["size"]
        total = math.ceil(entry["len"] / size)
        cur = int((state.get("pending") or {}).get(key, 0))
        if cur >= total:
            done.add(key)
            state["done"] = sorted(done)
            save_state(state)
            continue
        return {
            "key": key,
            "partIndex": cur,
            "totalParts": total,
            "expectedLen": entry["len"],
            "size": size,
            "use_figma_code": js_for(key, cur, size),
        }
    return None


def mark_part_done(key: str) -> None:
    state = load_state()
    pending = state.get("pending") or {}
    pending[key] = int(pending.get(key, 0)) + 1
    plan = {e["key"]: e for e in load_plan()}
    total = math.ceil(plan[key]["len"] / plan[key]["size"])
    if pending[key] >= total:
        pending.pop(key, None)
        done = set(state.get("done") or [])
        done.add(key)
        state["done"] = sorted(done)
    state["pending"] = pending
    save_state(state)


def finalize() -> None:
    subprocess.run([sys.executable, str(ROOT / "scripts/materialize-snapshot-from-mcp.py")], check=True)
    subprocess.run([sys.executable, str(ROOT / "scripts/assemble-mcp-snapshot-raw.py")], check=True)


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "ingest-slice":
        payload = json.loads(sys.stdin.read())
        subprocess.run(
            [
                sys.executable,
                str(INGEST),
                "--key",
                payload["key"],
                "--part-index",
                str(payload["partIndex"]),
                "--total-parts",
                str(payload["totalParts"]),
                "--expected-len",
                str(payload.get("expectedLen") or 0),
                "--slice",
                payload["slice"],
            ],
            check=True,
        )
        mark_part_done(payload["key"])
        job = next_job()
        print(json.dumps({"ingested": payload["key"], "next": job}, indent=2))
        if job is None:
            finalize()
            print("FINALIZED")
        return 0

    job = next_job()
    if job is None:
        finalize()
        print(json.dumps({"status": "complete"}))
        return 0
    print(json.dumps(job, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
