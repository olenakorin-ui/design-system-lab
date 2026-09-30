#!/usr/bin/env python3
"""Print use_figma JS for one component-set detail batch (reads cs-detail-batches.json)."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "design-system/snapshots/_raw/batches/inventories/_staging/cs-detail-batches.json"

PACK = """
async function pack(id, fullProps) {
  const n = await figma.getNodeByIdAsync(id);
  if (!n || n.type !== 'COMPONENT_SET') return null;
  const page = n.parent && n.parent.type === 'PAGE' ? n.parent.name : null;
  const variants = [];
  for (const c of n.children) {
    if (c.type !== 'COMPONENT') continue;
    const props = fullProps ? (c.componentProperties || {}) : {};
    variants.push({
      id: c.id, key: c.key || null, name: c.name, description: c.description || '',
      componentProperties: props
    });
  }
  const defs = {};
  for (const [k, v] of Object.entries(n.componentPropertyDefinitions || {})) {
    const d = { type: v.type };
    if (v.defaultValue !== undefined) d.defaultValue = v.defaultValue;
    if (v.variantOptions) d.variantOptions = v.variantOptions;
    defs[k] = d;
  }
  return {
    id: n.id, key: n.key || null, name: n.name, description: n.description || '',
    page,
    componentPropertyDefinitions: defs,
    defaultVariantId: n.defaultVariant ? n.defaultVariant.id : null,
    variants
  };
}
"""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--batch", type=int, required=True)
    p.add_argument("--full-props", action="store_true", help="Include per-variant componentProperties (large)")
    p.add_argument("--tsv", action="store_true", help="Return compact TSV of sets instead of JSON b64")
    args = p.parse_args()
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    batches = plan["batches"]
    if args.batch < 0 or args.batch >= len(batches):
        raise SystemExit(f"batch {args.batch} out of range 0..{len(batches)-1}")
    ids = batches[args.batch]
    inv_json = json.dumps(ids)
    full = "true" if args.full_props else "false"
    if args.tsv:
        code = (
            PACK
            + f"\nconst ids = {inv_json};\n"
            + f"const fullProps = {full};\n"
            + "const items = [];\n"
            + "for (const id of ids) { const x = await pack(id, fullProps); if (x) items.push(x); }\n"
            + "function esc(s){return String(s||'').replace(/\\t/g,' ').replace(/\\n/g,' ');}\n"
            + "const lines = items.map(s => {\n"
            + "  const prop = JSON.stringify(s.componentPropertyDefinitions);\n"
            + "  const vars = s.variants.map(v => v.id+'|'+esc(v.key)+'|'+esc(v.name)).join(';');\n"
            + "  return [s.id, esc(s.key), esc(s.name), esc(s.page), esc(s.defaultVariantId), prop, vars].join('\\t');\n"
            + "});\n"
            + "return { count: items.length, requested: ids.length, tsv: lines.join('\\n') };\n"
        )
    else:
        code = (
            PACK
            + f"\nconst ids = {inv_json};\n"
            + f"const fullProps = {full};\n"
            + "const items = [];\n"
            + "for (const id of ids) { const x = await pack(id, fullProps); if (x) items.push(x); }\n"
            + "const b64 = btoa(unescape(encodeURIComponent(JSON.stringify(items))));\n"
            + "return { count: items.length, requested: ids.length, b64Len: b64.length, b64 };\n"
        )
    print(code)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
