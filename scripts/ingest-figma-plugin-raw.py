#!/usr/bin/env python3
"""Ingest Figma plugin raw export into Snapshot v1 pipeline.

Usage:
  # Copy downloaded plugin file into place (or pass --raw):
  python3 scripts/ingest-figma-plugin-raw.py \\
    --raw path/to/figma-snapshot.raw.json

  # Validate completeness only:
  python3 scripts/ingest-figma-plugin-raw.py --raw ... --check-only

  # Normalize + validate after ingest:
  python3 scripts/ingest-figma-plugin-raw.py --raw ... --normalize --validate

Writes:
  design-system/snapshots/_raw/figma-snapshot.raw.json
  design-system/snapshots/_raw/figma-export.latest.json  (adapter for normalize-ds-snapshot.py)

Does NOT invent Figma data. Incomplete plugin payloads are rejected.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "design-system" / "snapshots" / "_raw"
PLUGIN_RAW = RAW_DIR / "figma-snapshot.raw.json"
EXPORT_LATEST = RAW_DIR / "figma-export.latest.json"

# Reference baselines from Sprint 01 inventory (not hard schema requirements)
REFERENCE = {
    "variables": 760,
    "componentSets": 405,
    "components": 285,
    "textStyles": 309,
    "effectStyles": 34,
    "icons": 1468,
}


def dump(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def load_raw(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("raw export must be a JSON object")
    return data


def check_complete(raw: dict) -> list[str]:
    errors: list[str] = []
    exporter = raw.get("exporter") or {}
    if exporter.get("schemaVersion") not in ("1.0-raw", "1.0"):
        errors.append(f"unexpected exporter.schemaVersion: {exporter.get('schemaVersion')}")
    file_meta = raw.get("file") or {}
    if not file_meta.get("key"):
        errors.append("file.key missing (plugin must run as private plugin with enablePrivatePluginApi)")
    if not file_meta.get("name"):
        errors.append("file.name missing")

    for key in ("collections", "variables", "componentSets", "components"):
        if not isinstance(raw.get(key), list):
            errors.append(f"missing array: {key}")

    styles = raw.get("styles") or {}
    for key in ("text", "effect", "paint", "grid"):
        if not isinstance(styles.get(key), list):
            errors.append(f"missing styles.{key} array")

    icons = raw.get("icons") or {}
    if not isinstance(icons.get("icons"), list):
        errors.append("missing icons.icons array")

    for s in raw.get("componentSets") or []:
        if not s.get("id") or not s.get("name"):
            errors.append("component set missing id/name")
            break
        if not isinstance(s.get("variants"), list):
            errors.append(f"component set {s.get('id')} missing variants")
            break
        # defaultVariantId may be null for empty sets, but key must exist after pack
        if "defaultVariantId" not in s and "defaultVariant" not in s:
            errors.append(f"component set {s.get('id')} missing defaultVariantId")
            break

    return errors


def reference_report(raw: dict) -> dict[str, dict]:
    styles = raw.get("styles") or {}
    icons = raw.get("icons") or {}
    icon_list = icons.get("icons") or []
    icon_ids = {i.get("id") for i in icon_list if i.get("id")}
    # Raw A/B exports may dual-list Icons-page nodes under components[];
    # inventory baseline is standalone non-icon only.
    standalone = [
        c
        for c in (raw.get("components") or [])
        if c.get("id") not in icon_ids
        and (c.get("page") if not isinstance(c.get("page"), dict) else (c.get("page") or {}).get("name"))
        != "Icons"
    ]
    actual = {
        "variables": len(raw.get("variables") or []),
        "componentSets": len(raw.get("componentSets") or []),
        "components": len(standalone),
        "textStyles": len(styles.get("text") or []),
        "effectStyles": len(styles.get("effect") or []),
        "icons": len(icon_list),
    }
    out = {}
    for k, ref in REFERENCE.items():
        a = actual.get(k, 0)
        out[k] = {"reference": ref, "actual": a, "delta": a - ref}
    return out


def adapt_for_normalize(raw: dict) -> dict:
    """Map plugin raw → shape expected by normalize-ds-snapshot.py."""
    return {
        "file": {
            "key": (raw.get("file") or {}).get("key"),
            "name": (raw.get("file") or {}).get("name"),
        },
        "sourceCapabilities": raw.get("sourceCapabilities")
        or {
            "variables": "complete",
            "components": "complete",
            "styles": "complete",
            "icons": "complete",
            "previews": "deferred",
            "structuralAudit": "deferred",
        },
        "extractionNotes": raw.get("extractionNotes")
        or {
            "transport": "figma-plugin",
            "iconsScope": "Icons page only",
        },
        "exporter": raw.get("exporter"),
        "collections": raw.get("collections") or [],
        "variables": raw.get("variables") or [],
        "styles": raw.get("styles")
        or {"text": [], "effect": [], "paint": [], "grid": []},
        "componentSets": raw.get("componentSets") or [],
        "components": raw.get("components") or [],
        "icons": raw.get("icons") or {"page": {"id": None, "name": "Icons"}, "icons": []},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--raw",
        type=Path,
        default=None,
        help="Path to downloaded figma-snapshot.raw.json (default: design-system/snapshots/_raw/figma-snapshot.raw.json)",
    )
    parser.add_argument("--check-only", action="store_true")
    parser.add_argument("--normalize", action="store_true", help="Run normalize-ds-snapshot.py after ingest")
    parser.add_argument("--validate", action="store_true", help="Run validate-ds-snapshot.py after normalize")
    parser.add_argument("--captured-at", default=None)
    args = parser.parse_args()

    src = args.raw or PLUGIN_RAW
    if not src.exists():
        print(f"ERROR: raw file not found: {src}", file=sys.stderr)
        print(
            "Export from the Figma plugin (tools/figma-snapshot-plugin) and place the file at:\n"
            f"  {PLUGIN_RAW}",
            file=sys.stderr,
        )
        return 2

    raw = load_raw(src)
    errors = check_complete(raw)
    report = reference_report(raw)

    print("REFERENCE DELTA")
    for k, row in report.items():
        print(f"  {k}: reference={row['reference']} actual={row['actual']} delta={row['delta']:+d}")

    if errors:
        print("INCOMPLETE — refusing ingest:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 3

    print("COMPLETENESS: ok")

    if args.check_only:
        return 0

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    if src.resolve() != PLUGIN_RAW.resolve():
        shutil.copy2(src, PLUGIN_RAW)
        print(f"Wrote {PLUGIN_RAW}")
    else:
        print(f"Using {PLUGIN_RAW}")

    adapted = adapt_for_normalize(raw)
    EXPORT_LATEST.write_text(dump(adapted), encoding="utf-8")
    print(f"Wrote {EXPORT_LATEST}")

    if args.normalize:
        cmd = [sys.executable, str(ROOT / "scripts" / "normalize-ds-snapshot.py"), "--raw", str(EXPORT_LATEST)]
        if args.captured_at:
            cmd.extend(["--captured-at", args.captured_at])
        print("Running normalize-ds-snapshot.py…")
        r = subprocess.run(cmd)
        if r.returncode != 0:
            return r.returncode

    if args.validate:
        print("Running validate-ds-snapshot.py…")
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate-ds-snapshot.py")])
        if r.returncode != 0:
            return r.returncode

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
