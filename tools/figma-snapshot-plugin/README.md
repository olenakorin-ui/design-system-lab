# Design System Snapshot — Figma Plugin v0.1

Read-only local plugin that exports a complete **raw** Snapshot v1 JSON from the open Figma file.

## Role

| Layer | Responsibility |
| --- | --- |
| **This plugin** | Read · serialize · export `figma-snapshot.raw.json` |
| **Repo** (`scripts/ingest-figma-plugin-raw.py`, `normalize-ds-snapshot.py`, `validate-ds-snapshot.py`) | Normalize · sort · validate · map · hash · diff |

Figma MCP is **not** used for bulk snapshot transport (≈20 KB truncation). Use MCP for targeted inspection/audit only.

## Install (Figma Desktop)

1. Open **Figma Desktop** → Design System V2.
2. Menu: **Plugins → Development → Import plugin from manifest…**
3. Select:

   `tools/figma-snapshot-plugin/manifest.json`

4. Run **Plugins → Development → Design System Snapshot**.

`enablePrivatePluginApi` is set so `figma.fileKey` is available for private/local plugins. Without a file key the export is marked **incomplete** and cannot be downloaded as a valid snapshot.

## Export

1. Confirm **Source** shows the correct file name.
2. Click **Export snapshot**.
3. Wait for progress (pages → variables → styles → components).
4. On success: **Snapshot ready** → **Download JSON**.
5. Save as:

   `design-system/snapshots/_raw/figma-snapshot.raw.json`

6. On failure: **Snapshot incomplete** — fix the listed category; do not treat partial JSON as canonical.

## Ingest in the repo

```bash
python3 scripts/ingest-figma-plugin-raw.py \
  --raw design-system/snapshots/_raw/figma-snapshot.raw.json \
  --normalize \
  --validate
```

Determinism check (export twice from unchanged Figma as A and B):

```bash
python3 scripts/ingest-figma-plugin-raw.py --raw /path/to/A.json --normalize
cp -R design-system/snapshots/latest /tmp/snap-a
# export B, then:
python3 scripts/ingest-figma-plugin-raw.py --raw /path/to/B.json --normalize
diff -rq /tmp/snap-a design-system/snapshots/latest
# contentHash in manifest.json must match
```

## Safety

- Read-only: no node create/edit/rename, no variable writes, no publish.
- Icons: only nodes on the page named exactly `Icons`.
- Component sets: `defaultVariantId` is taken from `ComponentSetNode.defaultVariant.id` (not a nonexistent `defaultVariantId` field).

## Reference inventory (current Design System V2)

Not hardcoded schema gates — used for delta reporting only:

| Category | Reference |
| --- | ---: |
| Variables | 760 |
| Component sets | 405 |
| Standalone components | 285 |
| Text styles | 309 |
| Effect styles | 34 |
| Icons page | 1468 |
