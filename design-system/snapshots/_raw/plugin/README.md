# Plugin raw exports

Sprint 01 A/B evidence (do not overwrite):

- `figma-snapshot.raw.A.json` — Export A (`exportedAt` 2026-09-30T07:45:20.813Z)
- `figma-snapshot.raw.B.json` — Export B (`exportedAt` 2026-09-30T08:58:14.676Z)

Working copy for the latest ingest also lands at:

`design-system/snapshots/_raw/figma-snapshot.raw.json`

Then run:

```bash
python3 scripts/ingest-figma-plugin-raw.py \
  --raw design-system/snapshots/_raw/plugin/figma-snapshot.raw.A.json \
  --normalize --validate
```

`exporter.exportedAt` is **not** part of canonical snapshot identity.
