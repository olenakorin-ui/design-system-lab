#!/usr/bin/env python3
"""Batch storage helpers for Design System Snapshot v1 extraction.

Validates MCP batch payloads, writes batch-XXXX.json + category manifests,
supports resume, and assembles figma-export.latest.json when complete.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
BATCH_ROOT = ROOT / "design-system" / "snapshots" / "_raw" / "batches"
RAW_ROOT = ROOT / "design-system" / "snapshots" / "_raw"
FILE_KEY = "ZllxQplWi5QJcNeUHeY8T3"
FILE_NAME = "Design System V2"

CATEGORIES = (
    "variables",
    "text-styles",
    "effect-styles",
    "components",
    "component-sets",
    "icons",
)

EXPECTED = {
    "variables": 760,
    "text-styles": 309,
    "effect-styles": 34,
    "icons": 1468,
    "component-sets": 405,
    # components: no reliable baseline — inventory-driven
    "components": None,
}


def dump(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def content_hash(obj: Any) -> str:
    body = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def category_dir(category: str) -> Path:
    d = BATCH_ROOT / category
    d.mkdir(parents=True, exist_ok=True)
    return d


def manifest_path(category: str) -> Path:
    return category_dir(category) / "manifest.json"


def load_manifest(category: str) -> dict:
    path = manifest_path(category)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    expected = EXPECTED.get(category)
    return {
        "category": category,
        "expectedCount": expected,
        "extractedCount": 0,
        "inventoryCount": 0,
        "completedBatches": [],
        "incompleteBatches": [],
        "retries": 0,
        "truncatedRejections": 0,
        "reducedSizeBatches": 0,
        "complete": False,
        "inventoryIds": [],
        "extractedIds": [],
        "missingIds": [],
        "duplicateIds": [],
        "batches": {},
    }


def save_manifest(manifest: dict) -> None:
    path = manifest_path(manifest["category"])
    path.write_text(dump(manifest), encoding="utf-8")


def validate_batch_payload(
    category: str,
    items: list[dict],
    *,
    requested_count: int | None = None,
) -> tuple[bool, str]:
    if not isinstance(items, list):
        return False, "items is not a list"
    if len(items) == 0:
        return False, "empty items"
    if requested_count is not None and len(items) > requested_count:
        return False, f"received {len(items)} > requested {requested_count}"
    ids: list[str] = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            return False, f"item[{i}] not an object"
        if "id" not in item or not item["id"]:
            return False, f"item[{i}] missing stable id"
        if "name" not in item:
            return False, f"item[{i}] missing name"
        ids.append(str(item["id"]))
    # terminal object complete: last item must have required keys for category
    last = items[-1]
    if category == "variables":
        for key in ("resolvedType", "valuesByMode", "variableCollectionId"):
            if key not in last:
                return False, f"terminal variable missing {key}"
    elif category in ("text-styles", "effect-styles"):
        if "styleType" not in last and "details" not in last:
            return False, "terminal style missing styleType/details"
    elif category == "component-sets":
        if "componentPropertyDefinitions" not in last and "variants" not in last:
            return False, "terminal component-set missing defs/variants"
    elif category == "components":
        if "componentSetId" not in last and "componentPropertyDefinitions" not in last:
            # standalone may omit set id — name+id enough if present
            pass
    elif category == "icons":
        if "type" not in last:
            return False, "terminal icon missing type"
    return True, "ok"


def write_batch(
    category: str,
    batch_index: int,
    items: list[dict],
    *,
    requested_count: int,
    retry_count: int = 0,
    status: str = "valid",
) -> dict:
    ok, reason = validate_batch_payload(category, items, requested_count=requested_count)
    if not ok:
        raise ValueError(f"reject batch {category}/{batch_index}: {reason}")

    ids = [str(i["id"]) for i in items]
    meta = {
        "category": category,
        "batchIndex": batch_index,
        "requestedCount": requested_count,
        "receivedCount": len(items),
        "firstStableId": ids[0],
        "lastStableId": ids[-1],
        "hash": content_hash(items),
        "retryCount": retry_count,
        "status": status,
        "ids": ids,
    }
    payload = {"meta": meta, "items": items}
    path = category_dir(category) / f"batch-{batch_index:04d}.json"
    path.write_text(dump(payload), encoding="utf-8")

    manifest = load_manifest(category)
    manifest["batches"][str(batch_index)] = {
        k: meta[k]
        for k in (
            "batchIndex",
            "requestedCount",
            "receivedCount",
            "firstStableId",
            "lastStableId",
            "hash",
            "retryCount",
            "status",
        )
    }
    if batch_index not in manifest["completedBatches"]:
        manifest["completedBatches"].append(batch_index)
    manifest["completedBatches"] = sorted(set(manifest["completedBatches"]))
    if batch_index in manifest["incompleteBatches"]:
        manifest["incompleteBatches"] = [b for b in manifest["incompleteBatches"] if b != batch_index]
    if retry_count:
        manifest["retries"] = int(manifest.get("retries") or 0) + retry_count
    # recompute extracted ids from all valid batches
    extracted: list[str] = []
    for idx in manifest["completedBatches"]:
        bpath = category_dir(category) / f"batch-{idx:04d}.json"
        if not bpath.exists():
            continue
        b = json.loads(bpath.read_text(encoding="utf-8"))
        extracted.extend(str(x["id"]) for x in b.get("items") or [])
    # detect duplicates
    seen: set[str] = set()
    dups: list[str] = []
    for eid in extracted:
        if eid in seen and eid not in dups:
            dups.append(eid)
        seen.add(eid)
    unique = sorted(seen)
    manifest["extractedIds"] = unique
    manifest["extractedCount"] = len(unique)
    manifest["duplicateIds"] = dups
    inv = manifest.get("inventoryIds") or []
    if inv:
        missing = sorted(set(inv) - set(unique))
        manifest["missingIds"] = missing
        expected = manifest.get("expectedCount")
        if expected is None:
            expected = len(inv)
        manifest["complete"] = len(missing) == 0 and len(dups) == 0 and len(unique) >= expected
    else:
        expected = manifest.get("expectedCount")
        if expected is not None:
            manifest["complete"] = len(unique) >= expected and len(dups) == 0
        else:
            manifest["complete"] = False
    save_manifest(manifest)
    return meta


def set_inventory(category: str, inventory: list[dict], *, expected: int | None = None) -> dict:
    """inventory items: {id, name, type?}"""
    if not inventory:
        # explicit empty inventory is allowed (e.g. no standalone components)
        pass
    elif not all(isinstance(i, dict) and i.get("id") and "name" in i for i in inventory):
        raise ValueError(f"invalid inventory for {category}: each item needs id+name")
    ids = [str(i["id"]) for i in inventory]
    if len(ids) != len(set(ids)):
        raise ValueError(f"inventory for {category} has duplicate ids")
    inv_path = BATCH_ROOT / "inventories" / f"{category}.json"
    inv_path.parent.mkdir(parents=True, exist_ok=True)
    inv_path.write_text(
        dump({"category": category, "count": len(inventory), "items": inventory}),
        encoding="utf-8",
    )
    manifest = load_manifest(category)
    manifest["inventoryIds"] = ids
    manifest["inventoryCount"] = len(ids)
    if expected is not None:
        manifest["expectedCount"] = expected
    elif EXPECTED.get(category) is not None:
        manifest["expectedCount"] = EXPECTED[category]
    else:
        manifest["expectedCount"] = len(ids)
    missing = sorted(set(ids) - set(manifest.get("extractedIds") or []))
    manifest["missingIds"] = missing
    extracted = set(manifest.get("extractedIds") or [])
    manifest["complete"] = (
        len(ids) > 0
        and len(missing) == 0
        and len(manifest.get("duplicateIds") or []) == 0
        and len(extracted) == len(ids)
    )
    save_manifest(manifest)
    return manifest


def mark_truncation(category: str, batch_index: int, *, reduced: bool = False) -> None:
    manifest = load_manifest(category)
    manifest["truncatedRejections"] = int(manifest.get("truncatedRejections") or 0) + 1
    manifest["retries"] = int(manifest.get("retries") or 0) + 1
    if reduced:
        manifest["reducedSizeBatches"] = int(manifest.get("reducedSizeBatches") or 0) + 1
    if batch_index not in manifest["incompleteBatches"]:
        manifest["incompleteBatches"].append(batch_index)
    save_manifest(manifest)


def first_incomplete_batch(category: str) -> int:
    manifest = load_manifest(category)
    completed = set(manifest.get("completedBatches") or [])
    if not completed:
        return 0
    # contiguous from 0
    i = 0
    while i in completed:
        i += 1
    return i


def load_all_items(category: str) -> list[dict]:
    manifest = load_manifest(category)
    by_id: dict[str, dict] = {}
    conflicts: list[str] = []
    for idx in sorted(manifest.get("completedBatches") or []):
        path = category_dir(category) / f"batch-{idx:04d}.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data.get("items") or []:
            iid = str(item["id"])
            if iid in by_id:
                if content_hash(by_id[iid]) != content_hash(item):
                    conflicts.append(iid)
            else:
                by_id[iid] = item
    if conflicts:
        raise RuntimeError(f"DECISION REQUIRED: conflicting duplicate IDs in {category}: {conflicts[:20]}")
    # preserve inventory order if present
    inv = manifest.get("inventoryIds") or []
    if inv:
        return [by_id[i] for i in inv if i in by_id]
    return [by_id[i] for i in sorted(by_id.keys())]


def write_extraction_manifest() -> dict:
    categories = {}
    all_complete = True
    for cat in CATEGORIES:
        m = load_manifest(cat)
        entry = {
            "expected": m.get("expectedCount"),
            "extracted": m.get("extractedCount", 0),
            "inventory": m.get("inventoryCount", 0),
            "missing": len(m.get("missingIds") or []),
            "duplicates": len(m.get("duplicateIds") or []),
            "complete": bool(m.get("complete")),
            "completedBatches": len(m.get("completedBatches") or []),
            "incompleteBatches": len(m.get("incompleteBatches") or []),
            "retries": m.get("retries", 0),
            "truncatedRejections": m.get("truncatedRejections", 0),
            "reducedSizeBatches": m.get("reducedSizeBatches", 0),
        }
        categories[cat] = entry
        # components: empty inventory is incomplete until set-inventory with ids
        if not entry["complete"]:
            all_complete = False
    out = {
        "fileKey": FILE_KEY,
        "fileName": FILE_NAME,
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "allComplete": all_complete,
        "categories": categories,
    }
    path = RAW_ROOT / "extraction-manifest.json"
    path.write_text(dump(out), encoding="utf-8")
    return out


def assemble_raw(force: bool = False) -> Path:
    em = write_extraction_manifest()
    if not em["allComplete"] and not force:
        raise RuntimeError("ASSEMBLY GATE: not all categories complete")

    variables = load_all_items("variables")
    # collections from variables batch sidecar or separate file
    collections_path = category_dir("variables") / "collections.json"
    if not collections_path.exists():
        raise RuntimeError("missing variables/collections.json")
    collections = json.loads(collections_path.read_text(encoding="utf-8"))
    if isinstance(collections, dict) and "collections" in collections:
        collections = collections["collections"]

    text = load_all_items("text-styles")
    effect = load_all_items("effect-styles")
    components = load_all_items("components") if (BATCH_ROOT / "components" / "manifest.json").exists() else []
    # allow empty components
    try:
        components = load_all_items("components")
    except Exception:
        components = []
    component_sets = load_all_items("component-sets")
    icons = load_all_items("icons")
    icons_page = {"id": None, "name": "Icons"}
    page_path = category_dir("icons") / "page.json"
    if page_path.exists():
        icons_page = json.loads(page_path.read_text(encoding="utf-8"))

    raw = {
        "file": {"key": FILE_KEY, "name": FILE_NAME},
        "sourceCapabilities": {
            "variables": "complete",
            "components": "complete",
            "styles": "complete",
            "icons": "complete",
            "previews": "deferred",
            "structuralAudit": "deferred",
        },
        "extractionNotes": {
            "transport": "batched-mcp",
            "iconsScope": "Icons page only",
        },
        "collections": collections,
        "variables": variables,
        "styles": {
            "text": text,
            "effect": effect,
            "paint": [],
            "grid": [],
        },
        "components": components,
        "componentSets": component_sets,
        "icons": {
            "page": icons_page,
            "icons": icons,
        },
    }
    out = RAW_ROOT / "figma-export.latest.json"
    out.write_text(dump(raw), encoding="utf-8")
    return out


def seed_variables_from_live() -> None:
    src = ROOT / "design-system" / "snapshots" / "_raw" / "mcp" / "variables-from-live.json"
    data = json.loads(src.read_text(encoding="utf-8"))
    collections = data["collections"]
    variables = data["variables"]
    inv = [{"id": v["id"], "name": v["name"], "type": v.get("resolvedType")} for v in variables]
    set_inventory("variables", inv, expected=760)
    collections_path = category_dir("variables") / "collections.json"
    collections_path.write_text(dump({"collections": collections}), encoding="utf-8")
    # write in batches of 100
    batch_size = 100
    for i in range(0, len(variables), batch_size):
        chunk = variables[i : i + batch_size]
        write_batch("variables", i // batch_size, chunk, requested_count=batch_size, retry_count=0)
    write_extraction_manifest()


def seed_icons_from_mcp() -> None:
    src = ROOT / "design-system" / "snapshots" / "_raw" / "mcp" / "icons.json"
    icons = json.loads(src.read_text(encoding="utf-8"))
    inv = [{"id": i["id"], "name": i["name"], "type": i.get("type")} for i in icons]
    set_inventory("icons", inv, expected=1468)
    page_path = category_dir("icons") / "page.json"
    page_path.write_text(dump({"id": None, "name": "Icons"}), encoding="utf-8")
    batch_size = 100
    for i in range(0, len(icons), batch_size):
        chunk = icons[i : i + batch_size]
        write_batch("icons", i // batch_size, chunk, requested_count=batch_size)
    write_extraction_manifest()


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_write = sub.add_parser("write-batch")
    p_write.add_argument("--category", required=True)
    p_write.add_argument("--index", type=int, required=True)
    p_write.add_argument("--requested", type=int, required=True)
    p_write.add_argument("--retry", type=int, default=0)
    p_write.add_argument("--file", type=Path, required=True, help="JSON file with {items:[...]}")

    p_inv = sub.add_parser("set-inventory")
    p_inv.add_argument("--category", required=True)
    p_inv.add_argument("--file", type=Path, required=True)
    p_inv.add_argument("--expected", type=int, default=None)

    p_trunc = sub.add_parser("mark-truncation")
    p_trunc.add_argument("--category", required=True)
    p_trunc.add_argument("--index", type=int, required=True)
    p_trunc.add_argument("--reduced", action="store_true")

    sub.add_parser("seed-variables")
    sub.add_parser("seed-icons")
    sub.add_parser("manifest")
    p_asm = sub.add_parser("assemble")
    p_asm.add_argument("--force", action="store_true")
    p_status = sub.add_parser("status")

    args = parser.parse_args()
    if args.cmd == "write-batch":
        data = json.loads(args.file.read_text(encoding="utf-8"))
        items = data["items"] if isinstance(data, dict) else data
        meta = write_batch(
            args.category,
            args.index,
            items,
            requested_count=args.requested,
            retry_count=args.retry,
        )
        print(json.dumps(meta))
        return 0
    if args.cmd == "set-inventory":
        data = json.loads(args.file.read_text(encoding="utf-8"))
        items = data["items"] if isinstance(data, dict) and "items" in data else data
        m = set_inventory(args.category, items, expected=args.expected)
        print(json.dumps({"inventoryCount": m["inventoryCount"], "complete": m["complete"]}))
        return 0
    if args.cmd == "mark-truncation":
        mark_truncation(args.category, args.index, reduced=args.reduced)
        return 0
    if args.cmd == "seed-variables":
        seed_variables_from_live()
        print("seeded variables")
        return 0
    if args.cmd == "seed-icons":
        seed_icons_from_mcp()
        print("seeded icons")
        return 0
    if args.cmd == "manifest":
        print(dump(write_extraction_manifest()))
        return 0
    if args.cmd == "assemble":
        path = assemble_raw(force=args.force)
        print(path)
        return 0
    if args.cmd == "status":
        print(dump(write_extraction_manifest()))
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
