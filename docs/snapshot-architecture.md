# Design System Snapshot — Architecture

## Purpose

Produce a **deterministic, versioned, machine-readable** snapshot of Figma Design System V2 for the Design System Lab repository.

Canonical artifacts live under:

```text
design-system/snapshots/
  schema/snapshot-v1.schema.json
  latest/{manifest,variables,components,styles,icons,mappings}.json
  history/<contentHash>/…
  _raw/
    figma-snapshot.raw.json      # plugin bulk export (source evidence)
    figma-export.latest.json     # adapted input for normalizer
    batches/…                    # MCP batch experiment evidence (fallback/audit)
    mcp/…                        # MCP extraction leftovers (fallback/audit)
```

## Transport architecture

```text
┌─────────────────────────────────────────────────────────┐
│  Figma Design System V2                                 │
└───────────────────────┬─────────────────────────────────┘
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
┌─────────────────────┐     ┌─────────────────────┐
│ Plugin (bulk)       │     │ Figma MCP (targeted)│
│ tools/figma-        │     │ inspection / audit  │
│ snapshot-plugin     │     │ debugging           │
│ READ · SERIALIZE ·  │     │ NOT full transport  │
│ EXPORT              │     └─────────────────────┘
└─────────┬───────────┘
          │ figma-snapshot.raw.json
          ▼
┌─────────────────────┐
│ ingest-figma-       │
│ plugin-raw.py       │
└─────────┬───────────┘
          │ figma-export.latest.json
          ▼
┌─────────────────────┐
│ normalize-ds-       │  sort · strip volatile · map
│ snapshot.py         │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ validate-ds-        │  schema · IDs · known checks
│ snapshot.py         │
└─────────┬───────────┘
          ▼
┌─────────────────────┐
│ latest/ + SHA-256   │  history/<hash>/ on change
│ contentHash         │
└─────────────────────┘
```

### Why the plugin is primary transport

Sprint 01 MCP experiments showed `use_figma` / MCP responses **truncate at approximately 20 KB**. Full inventories (760 variables, 309 text styles, 405 component sets with variants, 1468 icons) cannot be returned in a single MCP payload. Batched MCP extraction is preserved under `_raw/batches/` and `_raw/mcp/` as **experiment evidence and fallback**, not the production path.

### MCP still used for

- Targeted component / property inspection (Button, Badge, Checkbox known checks)
- Structural audits and debugging
- Spot validation against a plugin export

## Responsibilities

| Owner | Does | Does not |
| --- | --- | --- |
| **Figma plugin** | Read document · serialize · download raw JSON | Mutate Figma · normalize · hash |
| **Repo scripts** | Ingest · normalize · validate · hash · history | Invent Figma entities · redesign tokens |
| **ChatGPT / UX** | Product decisions | Snapshot transport implementation |

## Raw vs canonical

- **Raw** (`figma-snapshot.raw.json`): exporter evidence; may include extra fields (`exporter`, `documentationLinks`, `variantProperties`, `remote`).
- **Canonical** (`latest/*.json`): sorted, volatile-stripped, schema-aligned; **content hash excludes `capturedAt`**.

## Icons rule

Only `COMPONENT` / `COMPONENT_SET` nodes on the page named exactly **`Icons`** are classified as icons. No inference from names, sizes, or vectors.

## Component set default variant

Plugin and normalizer use:

```text
ComponentSetNode.defaultVariant.id  →  defaultVariantId
```

Do not assume a `defaultVariantId` field exists on the Plugin API object.

## Determinism

1. Export A and B from an unchanged Figma file via the plugin.
2. Ingest + normalize each.
3. Require `manifest.contentHash` A == B and `diff -rq` of canonical trees == 0.

## Commands

```bash
# After downloading plugin export:
python3 scripts/ingest-figma-plugin-raw.py \
  --raw design-system/snapshots/_raw/figma-snapshot.raw.json \
  --normalize --validate

# Or separately:
python3 scripts/normalize-ds-snapshot.py --raw design-system/snapshots/_raw/figma-export.latest.json
python3 scripts/validate-ds-snapshot.py
```

## Related

- Plugin: `tools/figma-snapshot-plugin/`
- Experiment log: `docs/experiments/design-system-snapshot-v1.md`
- Schema: `design-system/snapshots/schema/snapshot-v1.schema.json`
