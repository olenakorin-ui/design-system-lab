# Plugin raw exports

Place downloaded `figma-snapshot.raw.json` files here or at:

`design-system/snapshots/_raw/figma-snapshot.raw.json`

Then run:

```bash
python3 scripts/ingest-figma-plugin-raw.py --normalize --validate
```

For determinism, keep dated copies:

- `figma-snapshot.raw.A.json`
- `figma-snapshot.raw.B.json`
