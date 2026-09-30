#!/usr/bin/env python3
"""Print use_figma JS to pack component-set detail for a list of stable IDs."""
from __future__ import annotations

import argparse
import json
import sys

PACK = """
async function pack(id) {
  const n = await figma.getNodeByIdAsync(id);
  if (!n || n.type !== 'COMPONENT_SET') return null;
  const page = n.parent && n.parent.type === 'PAGE' ? n.parent.name : null;
  const variants = [];
  for (const c of n.children) {
    if (c.type !== 'COMPONENT') continue;
    variants.push({ id: c.id, key: c.key || null, name: c.name, description: '', componentProperties: {} });
  }
  const defs = {};
  for (const [k, v] of Object.entries(n.componentPropertyDefinitions || {})) {
    const d = { type: v.type };
    if (v.defaultValue !== undefined) d.defaultValue = v.defaultValue;
    if (v.variantOptions) d.variantOptions = v.variantOptions;
    defs[k] = d;
  }
  return { id: n.id, key: n.key || null, name: n.name, description: n.description || '', page, componentPropertyDefinitions: defs, defaultVariantId: n.defaultVariant ? n.defaultVariant.id : null, variants };
}
"""


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--ids", nargs="+", required=True)
    p.add_argument("--json-items", action="store_true", help="Return items if small else b64 chunks")
    p.add_argument("--tsv", action="store_true", help="Return compact TSV (smaller for large variant sets)")
    args = p.parse_args()
    inv = json.dumps(args.ids)
    if args.tsv:
        tail = (
            f"\nconst ids = {inv};\n"
            "const items = [];\n"
            "for (const id of ids) { const x = await pack(id); if (x) items.push(x); }\n"
            "function esc(s){return String(s||'').replace(/\\t/g,' ').replace(/\\n/g,' ');}\n"
            "const lines = items.map(s => {\n"
            "  const prop = JSON.stringify(s.componentPropertyDefinitions);\n"
            "  const vars = s.variants.map(v => v.id+'|'+esc(v.key)+'|'+esc(v.name)).join(';');\n"
            "  return [s.id, esc(s.key), esc(s.name), esc(s.page), esc(s.defaultVariantId), prop, vars].join('\\t');\n"
            "});\n"
            "const tsv = lines.join('\\n');\n"
            "if (tsv.length <= 15000) return { count: items.length, requested: ids.length, tsv };\n"
            "const chunks = [];\n"
            "let buf = [];\n"
            "let len = 0;\n"
            "for (const line of lines) {\n"
            "  if (len + line.length + 1 > 12000 && buf.length) {\n"
            "    chunks.push(buf.join('\\n'));\n"
            "    buf = [];\n"
            "    len = 0;\n"
            "  }\n"
            "  buf.push(line);\n"
            "  len += line.length + 1;\n"
            "}\n"
            "if (buf.length) chunks.push(buf.join('\\n'));\n"
            "return { count: items.length, requested: ids.length, tsvLen: tsv.length, tsvChunks: chunks };\n"
        )
    elif args.json_items:
        tail = (
            f"\nconst ids = {inv};\n"
            "const items = [];\n"
            "for (const id of ids) { const x = await pack(id); if (x) items.push(x); }\n"
            "const raw = JSON.stringify({ items });\n"
            "if (raw.length <= 15000) return { count: items.length, requested: ids.length, items };\n"
            "const b64 = btoa(unescape(encodeURIComponent(JSON.stringify(items))));\n"
            "const CH = 12000;\n"
            "const chunks = [];\n"
            "for (let i = 0; i < b64.length; i += CH) chunks.push(b64.slice(i, i + CH));\n"
            "return { count: items.length, requested: ids.length, b64Len: b64.length, b64Chunks: chunks };\n"
        )
    else:
        tail = (
            f"\nconst ids = {inv};\n"
            "const items = [];\n"
            "for (const id of ids) { const x = await pack(id); if (x) items.push(x); }\n"
            "const b64 = btoa(unescape(encodeURIComponent(JSON.stringify(items))));\n"
            "const CH = 12000;\n"
            "const chunks = [];\n"
            "for (let i = 0; i < b64.length; i += CH) chunks.push(b64.slice(i, i + CH));\n"
            "return { count: items.length, requested: ids.length, b64Len: b64.length, b64Chunks: chunks };\n"
        )
    sys.stdout.write(PACK + tail)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
