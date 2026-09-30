#!/usr/bin/env python3
"""Emit read-only use_figma JS for inventory-ordered detail batches."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEXT_PACK = """
const packText = (s) => ({
  id: s.id,
  key: s.key,
  name: s.name,
  description: s.description || '',
  styleType: 'TEXT',
  details: {
    fontSize: s.fontSize,
    fontName: s.fontName,
    lineHeight: s.lineHeight,
    letterSpacing: s.letterSpacing,
    textCase: s.textCase,
    textDecoration: s.textDecoration,
    paragraphSpacing: s.paragraphSpacing,
    paragraphIndent: s.paragraphIndent,
  },
});
"""

EFFECT_PACK = ""  # effect uses getLocalEffectStylesAsync map


def load_ids(category: str) -> list[str]:
    inv = ROOT / f"design-system/snapshots/_raw/batches/inventories/{category}.json"
    data = json.loads(inv.read_text(encoding="utf-8"))
    return [str(i["id"]) for i in data["items"]]


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--category", required=True, choices=("text-styles", "effect-styles", "component-sets", "components"))
    p.add_argument("--start", type=int, required=True)
    p.add_argument("--requested", type=int, required=True)
    p.add_argument("--b64-slice-index", type=int, default=None)
    p.add_argument("--b64-slice-size", type=int, default=500)
    args = p.parse_args()
    ids = load_ids(args.category)
    slice_ids = ids[args.start : args.start + args.requested]
    inv_json = json.dumps(slice_ids)
    if args.b64_slice_index is not None:
        ret = f"""
const b64 = btoa(unescape(encodeURIComponent(json)));
const SLICE_SIZE = {args.b64_slice_size};
const partIndex = {args.b64_slice_index};
const totalParts = Math.ceil(b64.length / SLICE_SIZE) || 1;
return {{
  start,
  end: start + items.length,
  count: items.length,
  total: {len(ids)},
  partIndex,
  totalParts,
  expectedB64Len: b64.length,
  slice: b64.slice(partIndex * SLICE_SIZE, (partIndex + 1) * SLICE_SIZE),
}};"""
    else:
        ret = f"return {{ start, end: start + items.length, count: items.length, total: {len(ids)}, b64: btoa(unescape(encodeURIComponent(json))) }};"
    if args.category == "text-styles":
        print(
            f"""const INV = {inv_json};
const start = {args.start};
const requested = {args.requested};
const ids = INV.slice(0, requested);
const styles = await figma.getLocalTextStylesAsync();
const byId = Object.fromEntries(styles.map((s) => [s.id, s]));
{TEXT_PACK}
const items = ids.map((id) => {{
  const s = byId[id];
  if (!s) throw new Error('missing ' + id);
  return packText(s);
}});
const json = JSON.stringify(items);
{ret}"""
        )
    elif args.category == "component-sets":
        print(
            f"""const INV = {inv_json};
const start = {args.start};
const requested = {args.requested};
const ids = INV.slice(0, requested);
const items = [];
for (const id of ids) {{
  const node = await figma.getNodeByIdAsync(id);
  if (!node || node.type !== 'COMPONENT_SET') throw new Error('missing set ' + id);
  const page = node.parent && node.parent.type === 'PAGE' ? node.parent.name : '';
  const variants = [];
  for (const child of node.children) {{
    if (child.type !== 'COMPONENT') continue;
    variants.push({{
      id: child.id,
      key: child.key,
      name: child.name,
      description: child.description || '',
      componentProperties: child.componentProperties || {{}},
    }});
  }}
  items.push({{
    id: node.id,
    key: node.key,
    name: node.name,
    description: node.description || '',
    page,
    componentPropertyDefinitions: node.componentPropertyDefinitions || {{}},
    defaultVariantId: node.defaultVariant ? node.defaultVariant.id : null,
    variants,
  }});
}}
const json = JSON.stringify(items);
{ret}"""
        )
    else:
        raise SystemExit(f"unsupported category {args.category}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
