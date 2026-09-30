#!/usr/bin/env python3
"""Normalize raw Figma snapshot extraction into canonical Design System Snapshot v1.

Primary input (plugin transport):
  design-system/snapshots/_raw/figma-export.latest.json
  (produced by scripts/ingest-figma-plugin-raw.py from figma-snapshot.raw.json)

Legacy / experiment input:
  MCP batch assemblies under design-system/snapshots/_raw/ (fallback evidence)

Output: design-system/snapshots/latest/{manifest,variables,components,styles,icons,mappings}.json
        design-system/snapshots/history/<contentHash>/… when content changes

Volatile fields (timestamps, session IDs, temp URLs) are excluded from hashed content.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SNAP = ROOT / "design-system" / "snapshots"
RAW_DEFAULT = SNAP / "_raw" / "figma-export.latest.json"
LATEST = SNAP / "latest"
HISTORY = SNAP / "history"
MAPPINGS_SRC = ROOT / "tokens" / "mappings" / "figma-to-code.json"

SCHEMA_VERSION = "1.0"
EXPECTED_COLLECTIONS = ("TailwindCSS", "Theme", "Mode", "Custom")


def dump_canonical(obj: Any) -> str:
    """Deterministic JSON: sorted keys, stable separators, UTF-8, trailing newline."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"), indent=2) + "\n"


def write_canonical(path: Path, obj: Any) -> str:
    text = dump_canonical(obj)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return text


def content_hash(parts: dict[str, str]) -> str:
    """SHA-256 over canonical file bodies in fixed filename order (excludes capturedAt)."""
    h = hashlib.sha256()
    for name in sorted(parts.keys()):
        h.update(name.encode("utf-8"))
        h.update(b"\0")
        h.update(parts[name].encode("utf-8"))
        h.update(b"\0")
    return h.hexdigest()


def sort_by_id(items: list[dict], key: str = "id") -> list[dict]:
    return sorted(items, key=lambda x: str(x.get(key, "")))


def collection_short_name(name: str) -> str:
    """'1. TailwindCSS' → 'TailwindCSS' for expectation checks; preserve exact in data."""
    parts = name.split(". ", 1)
    return parts[1] if len(parts) == 2 else name


def normalize_variables(raw: dict) -> dict:
    collections_in = raw.get("collections") or []
    variables_in = raw.get("variables") or []

    collections = []
    for c in collections_in:
        modes = sort_by_id(
            [{"id": m["id"], "name": m["name"]} for m in (c.get("modes") or [])],
            "id",
        )
        collections.append(
            {
                "id": c["id"],
                "name": c["name"],
                "modes": modes,
                "variableIds": sorted(c.get("variableIds") or []),
            }
        )
    collections = sort_by_id(collections)

    variables = []
    for v in variables_in:
        values = v.get("valuesByMode") or {}
        # sort mode keys
        values_sorted = {k: values[k] for k in sorted(values.keys())}
        code_syntax = v.get("codeSyntax") or {}
        if not isinstance(code_syntax, dict):
            code_syntax = {}
        code_syntax = {k: code_syntax[k] for k in sorted(code_syntax.keys())}
        variables.append(
            {
                "id": v["id"],
                "name": v["name"],
                "resolvedType": v.get("resolvedType"),
                "description": v.get("description") if v.get("description") is not None else "",
                "scopes": sorted(v.get("scopes") or []),
                "codeSyntax": code_syntax,
                "valuesByMode": values_sorted,
                "variableCollectionId": v.get("variableCollectionId"),
            }
        )
    variables = sort_by_id(variables)

    return {
        "schemaVersion": SCHEMA_VERSION,
        "collections": collections,
        "variables": variables,
    }


def _page_name(page: object) -> str | None:
    if isinstance(page, dict):
        name = page.get("name")
        return str(name) if name is not None else None
    if page is None:
        return None
    return str(page)


def normalize_components(raw: dict, *, exclude_ids: set[str] | None = None) -> dict:
    """Normalize component sets + standalone non-icon components.

    Icons-page nodes belong in icons.json only. Raw plugin exports may still
    list them under components[]; exclude by Icons page name and/or icon ids.
    """
    sets_in = raw.get("componentSets") or []
    comps_in = raw.get("components") or []
    excluded = exclude_ids or set()

    component_sets = []
    for s in sets_in:
        props = s.get("componentPropertyDefinitions") or {}
        # stable key order for property definitions
        props_sorted = {k: props[k] for k in sorted(props.keys())}
        variants = sort_by_id(s.get("variants") or [])
        component_sets.append(
            {
                "id": s["id"],
                "key": s.get("key") if s.get("key") not in ("", None) else None,
                "name": s["name"],
                "description": s.get("description") if s.get("description") is not None else "",
                "page": s.get("page") or None,
                "componentPropertyDefinitions": props_sorted,
                "defaultVariantId": s.get("defaultVariantId") if s.get("defaultVariantId") else None,
                "variants": [
                    {
                        "id": v["id"],
                        "key": v.get("key") if v.get("key") not in ("", None) else None,
                        "name": v["name"],
                        "description": v.get("description") if v.get("description") is not None else "",
                        "componentProperties": {
                            k: (v.get("componentProperties") or {})[k]
                            for k in sorted((v.get("componentProperties") or {}).keys())
                        },
                    }
                    for v in variants
                ],
            }
        )
    component_sets = sort_by_id(component_sets)

    components = []
    for c in comps_in:
        cid = c.get("id")
        if cid in excluded:
            continue
        if _page_name(c.get("page")) == "Icons":
            continue
        components.append(
            {
                "id": c["id"],
                "key": c.get("key") if c.get("key") not in ("", None) else None,
                "name": c["name"],
                "description": c.get("description") if c.get("description") is not None else "",
                "page": c.get("page") or None,
                "componentSetId": c.get("componentSetId") if c.get("componentSetId") else None,
                "componentPropertyDefinitions": {
                    k: (c.get("componentPropertyDefinitions") or {})[k]
                    for k in sorted((c.get("componentPropertyDefinitions") or {}).keys())
                },
            }
        )
    components = sort_by_id(components)

    return {
        "schemaVersion": SCHEMA_VERSION,
        "componentSets": component_sets,
        "components": components,
    }


def normalize_styles(raw: dict) -> dict:
    def pack_style(s: dict) -> dict:
        return {
            "id": s["id"],
            "key": s.get("key") if s.get("key") not in ("", None) else None,
            "name": s["name"],
            "description": s.get("description") if s.get("description") is not None else "",
            "styleType": s.get("styleType"),
            "details": s.get("details") if s.get("details") is not None else {},
        }

    text = sort_by_id([pack_style(s) for s in (raw.get("text") or [])])
    effect = sort_by_id([pack_style(s) for s in (raw.get("effect") or [])])
    paint = sort_by_id([pack_style(s) for s in (raw.get("paint") or [])])
    grid = sort_by_id([pack_style(s) for s in (raw.get("grid") or [])])

    return {
        "schemaVersion": SCHEMA_VERSION,
        "text": text,
        "effect": effect,
        "paint": paint,
        "grid": grid,
    }


def normalize_icons(raw: dict) -> dict:
    icons = []
    for i in raw.get("icons") or []:
        icons.append(
            {
                "id": i["id"],
                "name": i["name"],
                "type": i.get("type"),
                "page": i.get("page") or "Icons",
                "description": i.get("description") if i.get("description") is not None else "",
            }
        )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "page": raw.get("page") or {"id": None, "name": "Icons"},
        "icons": sort_by_id(icons),
        "classification": "explicit-icons-page-only",
    }


def normalize_mappings() -> dict:
    if not MAPPINGS_SRC.exists():
        return {
            "schemaVersion": SCHEMA_VERSION,
            "source": "tokens/mappings/figma-to-code.json",
            "meta": {},
            "mappings": [],
        }
    src = json.loads(MAPPINGS_SRC.read_text(encoding="utf-8"))
    mappings = src.get("mappings") or []
    # stable order by figma path then codePath — do not rename entities
    mappings_sorted = sorted(
        mappings,
        key=lambda m: (str(m.get("figma", "")), str(m.get("codePath", "")), str(m.get("cssVar", ""))),
    )
    return {
        "schemaVersion": SCHEMA_VERSION,
        "source": "tokens/mappings/figma-to-code.json",
        "meta": src.get("meta") or {},
        "mappings": mappings_sorted,
    }


def build_source_capabilities(raw: dict) -> dict:
    caps = raw.get("sourceCapabilities") or {}
    defaults = {
        "variables": "complete",
        "components": "partial",
        "styles": "partial",
        "icons": "partial",
        "previews": "deferred",
        "structuralAudit": "deferred",
    }
    out = dict(defaults)
    out.update({k: v for k, v in caps.items() if v in ("complete", "partial", "unsupported", "deferred")})
    return {k: out[k] for k in sorted(out.keys())}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw", type=Path, default=RAW_DEFAULT)
    parser.add_argument("--captured-at", default=None, help="Optional ISO timestamp for manifest only")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.raw.exists():
        print(f"ERROR: raw export not found: {args.raw}", file=sys.stderr)
        return 2

    raw = json.loads(args.raw.read_text(encoding="utf-8"))
    file_meta = raw.get("file") or {}
    file_key = file_meta.get("key") or raw.get("fileKey")
    file_name = file_meta.get("name") or raw.get("fileName") or "Document"
    if not file_key:
        print("ERROR: missing file key in raw export", file=sys.stderr)
        return 2

    variables = normalize_variables(raw.get("variablesPayload") or raw)
    # support both nested and flat raw shapes
    if "collections" in raw and "variables" in raw and "variablesPayload" not in raw:
        variables = normalize_variables(raw)

    styles = normalize_styles(raw.get("stylesPayload") or raw.get("styles") or {})
    icons = normalize_icons(raw.get("iconsPayload") or raw.get("icons") or {})
    icon_ids = {i["id"] for i in icons.get("icons") or [] if i.get("id")}
    components = normalize_components(
        raw.get("componentsPayload") or raw,
        exclude_ids=icon_ids,
    )
    mappings = normalize_mappings()
    capabilities = build_source_capabilities(raw)

    # counts (canonical)
    counts = {
        "collections": len(variables["collections"]),
        "variables": len(variables["variables"]),
        "componentSets": len(components["componentSets"]),
        "components": len(components["components"]),
        "textStyles": len(styles["text"]),
        "effectStyles": len(styles["effect"]),
        "paintStyles": len(styles["paint"]),
        "gridStyles": len(styles["grid"]),
        "icons": len(icons["icons"]),
        "mappings": len(mappings["mappings"]),
    }

    # Hash excludes capturedAt / volatile metadata
    bodies = {
        "variables.json": dump_canonical(variables),
        "components.json": dump_canonical(components),
        "styles.json": dump_canonical(styles),
        "icons.json": dump_canonical(icons),
        "mappings.json": dump_canonical(mappings),
    }
    digest = content_hash(bodies)

    manifest = {
        "schemaVersion": SCHEMA_VERSION,
        "file": {"key": file_key, "name": file_name},
        "sourceCapabilities": capabilities,
        "counts": counts,
        "contentHash": digest,
        "files": sorted(bodies.keys()),
    }
    # capturedAt is metadata only — written after hash identity established
    if args.captured_at:
        manifest_with_time = dict(manifest)
        manifest_with_time["capturedAt"] = args.captured_at
    else:
        manifest_with_time = dict(manifest)
        manifest_with_time["capturedAt"] = None

    history_dir = HISTORY / digest
    unchanged = history_dir.exists() and (LATEST / "manifest.json").exists()
    if unchanged:
        try:
            prev = json.loads((LATEST / "manifest.json").read_text(encoding="utf-8"))
            unchanged = prev.get("contentHash") == digest
        except Exception:
            unchanged = False

    print(f"SNAPSHOT HASH: {digest}")
    if unchanged:
        print("SNAPSHOT UNCHANGED")
        # still refresh latest capturedAt? Spec: do not create duplicate history;
        # updating latest capturedAt would change git — skip writes entirely when unchanged
        if args.dry_run:
            return 0
        return 0

    print("SNAPSHOT CHANGED — writing latest + history")
    if args.dry_run:
        return 0

    # write latest
    LATEST.mkdir(parents=True, exist_ok=True)
    write_canonical(LATEST / "variables.json", variables)
    write_canonical(LATEST / "components.json", components)
    write_canonical(LATEST / "styles.json", styles)
    write_canonical(LATEST / "icons.json", icons)
    write_canonical(LATEST / "mappings.json", mappings)
    write_canonical(LATEST / "manifest.json", manifest_with_time)

    # history copy
    if history_dir.exists():
        shutil.rmtree(history_dir)
    shutil.copytree(LATEST, history_dir)

    print(f"Wrote {LATEST}")
    print(f"Wrote {history_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
