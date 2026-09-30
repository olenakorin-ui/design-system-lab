# Component-set detail extraction loop

1. `python3 scripts/snapshot-cs-pack-many.py --max-ids 24 > design-system/snapshots/_raw/batches/inventories/_staging/cs-pack-many.js`
2. Run `use_figma` with `fileKey=ZllxQplWi5QJcNeUHeY8T3`, `skillNames=figma-use`, code from `cs-pack-many.js`.
3. Save JSON: `python3 scripts/snapshot-save-mcp-response.py design-system/snapshots/_raw/batches/inventories/_staging/cs-mcp-response.json < mcp.json`
4. Ingest: read `startBatchIndex` from `cs-pack-many-meta.json`, then:
   `python3 scripts/snapshot-cs-ingest-figma-tsv-response.py --start-index <N> --response-file .../cs-mcp-response.json`
5. Repeat until `python3 -c "import json;from pathlib import Path;m=json.loads(Path('design-system/snapshots/_raw/batches/component-sets/manifest.json').read_text());print(len(m['missingIds']))"` prints `0`.

Single-set (Button-sized): `python3 scripts/snapshot-cs-pack-code.py --tsv --ids <id>`.

Queue: `design-system/snapshots/_raw/batches/inventories/_staging/cs-detail-queue.json`.
