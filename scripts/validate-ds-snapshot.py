#!/usr/bin/env python3
"""Validate canonical Design System Snapshot v1 artifacts.

Checks:
- JSON schema (manifest core)
- duplicate IDs
- missing alias references
- mapping collisions (same figma path → different code targets)
- expected collections
- known component property checks (Button / Badge / Checkbox)
- deterministic ordering
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LATEST = ROOT / "design-system" / "snapshots" / "latest"
SCHEMA = ROOT / "design-system" / "snapshots" / "schema" / "snapshot-v1.schema.json"

EXPECTED_COLLECTION_SUFFIXES = ("TailwindCSS", "Theme", "Mode", "Custom")
EXPECTED_BASELINE = {
    "collections": 4,
    "variables": 760,
    "componentSets": 405,
    "components": 285,
    "textStyles": 309,
    "effectStyles": 34,
    "paintStyles": 0,
    "gridStyles": 0,
    "icons": 1468,
}


def load(name: str) -> dict:
    path = LATEST / name
    if not path.exists():
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def is_sorted_by_id(items: list[dict], key: str = "id") -> bool:
    ids = [str(i.get(key, "")) for i in items]
    return ids == sorted(ids)


def find_component_set(components: dict, name: str) -> dict | None:
    for s in components.get("componentSets") or []:
        if s.get("name") == name:
            return s
    # also allow page-prefixed or nested names ending with name
    for s in components.get("componentSets") or []:
        if str(s.get("name", "")).endswith(name) or name in str(s.get("name", "")).split("/"):
            if s.get("name") == name or s.get("name").split("/")[-1] == name:
                return s
    return None


def property_option_values(prop_def: dict) -> list[str]:
    """Extract variant option names from a Figma componentPropertyDefinitions entry."""
    if not isinstance(prop_def, dict):
        return []
    # VARIANT type uses variantOptions
    opts = prop_def.get("variantOptions")
    if isinstance(opts, list):
        return [str(o) for o in opts]
    # sometimes nested
    if prop_def.get("type") == "VARIANT" and "variantOptions" in prop_def:
        return [str(o) for o in prop_def["variantOptions"]]
    return []


def main() -> int:
    global LATEST
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--latest", type=Path, default=LATEST)
    parser.add_argument("--strict-baseline", action="store_true", help="Fail if counts != known live audit")
    args = parser.parse_args()

    LATEST = args.latest

    errors: list[str] = []
    warnings: list[str] = []

    try:
        manifest = load("manifest.json")
        variables = load("variables.json")
        components = load("components.json")
        styles = load("styles.json")
        icons = load("icons.json")
        mappings = load("mappings.json")
    except FileNotFoundError as e:
        print(f"ERROR: missing snapshot file: {e}", file=sys.stderr)
        return 2

    # --- schema-ish manifest checks ---
    if manifest.get("schemaVersion") != "1.0":
        errors.append(f"manifest.schemaVersion expected 1.0, got {manifest.get('schemaVersion')}")
    if not manifest.get("file", {}).get("key"):
        errors.append("manifest.file.key missing")
    if not manifest.get("contentHash") or len(manifest["contentHash"]) != 64:
        errors.append("manifest.contentHash missing or not sha256 hex")

    # optional: draft-07 validate if jsonschema installed
    try:
        import jsonschema  # type: ignore

        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        # validate subset fields present on manifest
        jsonschema.validate(
            {
                "schemaVersion": manifest["schemaVersion"],
                "file": manifest["file"],
                "sourceCapabilities": manifest.get("sourceCapabilities") or {},
                "counts": manifest.get("counts") or {},
                "contentHash": manifest.get("contentHash"),
                "capturedAt": manifest.get("capturedAt"),
            },
            schema,
        )
    except ImportError:
        warnings.append("jsonschema not installed — skipped formal schema validation")
    except Exception as e:
        errors.append(f"schema validation failed: {e}")

    # --- collections ---
    cols = variables.get("collections") or []
    short = [c["name"].split(". ", 1)[-1] for c in cols]
    for expected in EXPECTED_COLLECTION_SUFFIXES:
        if expected not in short:
            errors.append(f"missing expected collection suffix: {expected}")

    # --- duplicate IDs ---
    for label, items in (
        ("variable", variables.get("variables") or []),
        ("collection", cols),
        ("componentSet", components.get("componentSets") or []),
        ("component", components.get("components") or []),
        ("textStyle", styles.get("text") or []),
        ("effectStyle", styles.get("effect") or []),
        ("icon", icons.get("icons") or []),
    ):
        seen: set[str] = set()
        for it in items:
            i = it.get("id")
            if not i:
                errors.append(f"{label} missing id")
                continue
            if i in seen:
                errors.append(f"duplicate {label} id: {i}")
            seen.add(i)

    # --- ordering ---
    if not is_sorted_by_id(variables.get("variables") or []):
        errors.append("variables not sorted by id")
    if not is_sorted_by_id(cols):
        errors.append("collections not sorted by id")
    if not is_sorted_by_id(components.get("componentSets") or []):
        errors.append("componentSets not sorted by id")
    if not is_sorted_by_id(components.get("components") or []):
        errors.append("components not sorted by id")
    if not is_sorted_by_id(styles.get("text") or []):
        errors.append("text styles not sorted by id")
    if not is_sorted_by_id(icons.get("icons") or []):
        errors.append("icons not sorted by id")

    # --- unresolved aliases ---
    var_ids = {v["id"] for v in variables.get("variables") or []}
    unresolved = []
    for v in variables.get("variables") or []:
        for mode, val in (v.get("valuesByMode") or {}).items():
            if isinstance(val, dict) and val.get("alias") is True:
                target = val.get("id")
                if target not in var_ids:
                    unresolved.append(f"{v['id']}@{mode} -> {target}")
    if unresolved:
        errors.append(f"unresolved aliases: {len(unresolved)} (expected 0)")
        for u in unresolved[:20]:
            errors.append(f"  alias: {u}")

    # --- mapping collisions ---
    by_figma: dict[str, list[dict]] = {}
    for m in mappings.get("mappings") or []:
        figma = m.get("figma")
        if not figma:
            continue
        by_figma.setdefault(figma, []).append(m)
    collisions = []
    for figma, rows in by_figma.items():
        targets = {(r.get("codePath"), r.get("cssVar")) for r in rows}
        if len(targets) > 1:
            collisions.append(figma)
    if collisions:
        # Known token-mapping debt (desktop/mobile + dual radius paths). Snapshot
        # integrity does not require 0 collisions; report as warnings for v1.
        warnings.append(
            f"mapping collisions: {len(collisions)} (documented token-mapping debt; not blocking Snapshot v1)"
        )
        for c in collisions[:20]:
            warnings.append(f"  mapping: {c}")

    # --- baseline counts ---
    counts = manifest.get("counts") or {}
    for k, expected in EXPECTED_BASELINE.items():
        actual = counts.get(k)
        if actual != expected:
            msg = f"count {k}: expected {expected}, got {actual}"
            if args.strict_baseline:
                errors.append(msg)
            else:
                warnings.append(msg)

    # --- known component checks ---
    button = find_component_set(components, "Button")
    if not button:
        errors.append("Button component set not found")
    else:
        props = button.get("componentPropertyDefinitions") or {}
        # Figma often uses Variant/State/Size as property names — accept case-insensitive keys
        prop_keys = {k.lower(): k for k in props.keys()}
        for need in ("variant", "state", "size"):
            if need not in prop_keys:
                # also accept nested in variantOptions axis naming from variant group names
                warnings.append(f"Button missing explicit property key matching '{need}' (keys={list(props.keys())})")
        # Collect variant option values across VARIANT props + variant node names
        variant_values: set[str] = set()
        for pname, pdef in props.items():
            if pname.lower() == "variant" or "variant" in pname.lower():
                variant_values.update(property_option_values(pdef))
        if not variant_values:
            for v in button.get("variants") or []:
                # name like "Variant=Default, State=Default, Size=Default"
                for part in str(v.get("name", "")).split(","):
                    part = part.strip()
                    if part.lower().startswith("variant="):
                        variant_values.add(part.split("=", 1)[1])
        expected_variants = {"Default", "Secondary", "Destructive", "Outline", "Ghost", "Link"}
        missing = expected_variants - variant_values
        if missing:
            errors.append(f"Button missing variants: {sorted(missing)} (found={sorted(variant_values)})")

    badge = find_component_set(components, "Badge")
    if not badge:
        errors.append("Badge component set not found")
    else:
        variant_values = set()
        props = badge.get("componentPropertyDefinitions") or {}
        for pname, pdef in props.items():
            if "variant" in pname.lower():
                variant_values.update(property_option_values(pdef))
        if not variant_values:
            for v in badge.get("variants") or []:
                for part in str(v.get("name", "")).split(","):
                    part = part.strip()
                    if part.lower().startswith("variant="):
                        variant_values.add(part.split("=", 1)[1])
        expected = {"Default", "Secondary", "Outline", "Destructive", "Verified"}
        missing = expected - variant_values
        if missing:
            errors.append(f"Badge missing variants: {sorted(missing)} (found={sorted(variant_values)})")

    checkbox = find_component_set(components, "Checkbox")
    if not checkbox:
        errors.append("Checkbox component set not found")
    else:
        states: set[str] = set()
        props = checkbox.get("componentPropertyDefinitions") or {}
        for pname, pdef in props.items():
            if "state" in pname.lower() or pname.lower() in ("checked", "status"):
                states.update(property_option_values(pdef))
        if not states:
            for v in checkbox.get("variants") or []:
                for part in str(v.get("name", "")).split(","):
                    part = part.strip()
                    if "=" in part:
                        k, val = part.split("=", 1)
                        if k.strip().lower() in ("state", "checked", "status"):
                            states.add(val.strip())
        # Expected: Active, Inactive — NOT Indeterminate
        if "Indeterminate" in states:
            errors.append("Checkbox unexpectedly lists Indeterminate in Figma (should remain DS debt only)")
        for need in ("Active", "Inactive"):
            if need not in states and states:
                # Soft: some files use Checked/Unchecked
                warnings.append(f"Checkbox missing state '{need}' (found={sorted(states)})")
        if not states:
            warnings.append("Checkbox states could not be parsed from properties/variant names")

    # --- icons page rule ---
    if icons.get("classification") != "explicit-icons-page-only":
        errors.append("icons.classification must be explicit-icons-page-only")

    print("=== SNAPSHOT VALIDATION ===")
    print(f"contentHash: {manifest.get('contentHash')}")
    print(f"counts: {json.dumps(counts, sort_keys=True)}")
    print(f"unresolvedAliases: {len(unresolved)}")
    print(f"mappingCollisions: {len(collisions)}")
    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")

    if errors:
        print("VALIDATION FAILED")
        return 1
    print("VALIDATION PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
