# Experiment: Design System Snapshot V1

**Status:** CLOSED — Sprint 01 complete  
**Branch:** `ds/snapshot-v1`  
**Figma:** Design System V2 (`ZllxQplWi5QJcNeUHeY8T3`)  
**Snapshot Schema:** **v1.0 frozen**

## Goal

Deterministic, versioned, machine-readable snapshot of Design System V2:

```text
raw export → normalize → validate → SHA-256 → latest/ + history/
```

## Transport roles (frozen)

| Layer | Role |
| --- | --- |
| **Plugin** | Bulk Figma snapshot transport |
| **MCP** | Targeted inspection / structural audit |
| **Git** | Durable versioned canonical source |

## Experiment phases

### Phase A — Figma MCP bulk extraction (failed as primary transport)

**Hypothesis:** Figma MCP `use_figma` can return full inventories for a single raw export.

**Result:** **Rejected as primary transport.**

| Observation | Detail |
| --- | --- |
| MCP BULK TRANSPORT | **Failed at scale** due to ~**20 KB** response truncation |
| Symptom | Mid-JSON / mid-TSV cutoffs; incomplete terminal objects |
| Mitigation attempted | Batched extraction, TSV, base64 slices, inventory-first, resumable manifests under `design-system/snapshots/_raw/batches/` |
| Outcome | Variables + icons + text + effect largely recoverable via batches; **component-set details (~405)** impractical via MCP |

MCP inventories, batch manifests, and helper scripts are **retained** as fallback / audit / experiment evidence. Do not delete.

### Phase B — Figma Plugin exporter (PASS)

**Hypothesis:** Plugin API in Figma Desktop can scan the full file and download one complete `figma-snapshot.raw.json` without MCP size limits.

**Result:** **PASS**

| Item | Status |
| --- | --- |
| PLUGIN TRANSPORT | **PASS** |
| RAW EXPORT SIZE | **2,245,884 bytes** (A and B) |
| A/B RAW DIFFERENCE | `exporter.exportedAt` **only** |
| Live A/B export from Design System V2 | **Complete** |

`exportedAt` is **not** part of canonical snapshot identity.

## Inventory result (Design System V2)

| Category | Count |
| --- | ---: |
| Variables | 760 |
| Variable collections | 4 |
| Component sets | 405 |
| Standalone non-icon components | 285 |
| Text styles | 309 |
| Effect styles | 34 |
| Icons | 1468 |
| Paint styles | 0 |
| Grid styles | 0 |
| Pages | 64 |

### Icon model

| Icons page | Count |
| --- | ---: |
| COMPONENT | 1468 |
| COMPONENT_SET | 0 |
| Total | 1468 |

Reconciliation: `1753` total COMPONENT nodes − `1468` Icons-page = `285` standalone non-icon components.

### Aliases / IDs

| Check | Result |
| --- | --- |
| Variable alias references | 225 |
| Unresolved aliases | 0 |
| Duplicate IDs | 0 |
| Component sets missing `defaultVariantId` | 0 |
| Stable ID sets A vs B | identical (variables, text, effect, components, sets, icons) |

## Figma export determinism (source)

| Metric | A | B |
| --- | --- | --- |
| Raw SHA-256 | `3c16804cafc0ae141d7a7e2a20945b5df350bbaebbfa2ce7a3fbf2694b085204` | `c41e0d19d3c9cf48cc56961dbec6ba38c28a31cda65eb92b3a67afbe5853d999` |
| exportedAt | `2026-09-30T07:45:20.813Z` | `2026-09-30T08:58:14.676Z` |
| SOURCE SEMANTIC HASH | `4f262fe450cbf5f1755fae243d4cdc9aa0468a6bbba8d12847e8edc22940fb93` | `4f262fe450cbf5f1755fae243d4cdc9aa0468a6bbba8d12847e8edc22940fb93` |

SOURCE SEMANTIC DIFF: **0**  
FIGMA EXPORT DETERMINISM: **PASS**

Evidence preserved at:

- `design-system/snapshots/_raw/plugin/figma-snapshot.raw.A.json`
- `design-system/snapshots/_raw/plugin/figma-snapshot.raw.B.json`

## Repository canonical determinism

Ingest pipeline: `scripts/ingest-figma-plugin-raw.py --normalize --validate`

| Metric | A | B |
| --- | --- | --- |
| Ingest | PASS | PASS |
| Schema | v1.0 (manifest `schemaVersion`) | v1.0 |
| Validation | PASS (mapping collisions → warnings) | PASS |
| CANONICAL HASH | `b9d6dcf77e1b452755b6100eca75ca318560adef871cecf45655f4cc53db0de2` | `b9d6dcf77e1b452755b6100eca75ca318560adef871cecf45655f4cc53db0de2` |

CANONICAL DIFF: **0** (`diff -rq` identical)  
CANONICAL DETERMINISM: **PASS**

History: `design-system/snapshots/history/b9d6dcf77e1b452755b6100eca75ca318560adef871cecf45655f4cc53db0de2/`

## Snapshot Schema freeze

**Snapshot Schema v1.0** is frozen for Sprint 01.

- Canonical files: `latest/{manifest,variables,components,styles,icons,mappings}.json`
- Content hash excludes `capturedAt` and raw `exporter.exportedAt`
- Icons classification: `explicit-icons-page-only`
- Standalone `components` exclude Icons-page nodes

## Known limitations (Sprint 01)

1. Formal `jsonschema` Python package not installed in the default env — formal schema check skipped (WARN); structural validator still runs.
2. **13 mapping collisions** in `tokens/mappings/figma-to-code.json` (desktop/mobile dual paths + dual radius/white). Reported as warnings; not blocking Snapshot v1 integrity.
3. Raw plugin exports A/B still dual-list Icons-page nodes under `components[]` (1753). Normalizer strips them to 285. Plugin code fixed for **future** exports; A/B evidence left unchanged.
4. Previews and deep structural audit remain deferred (MCP / later sprints).

## Manual corrections / prompt iterations

1. MCP → batched TSV/b64 — still truncated for large CS payloads.
2. Abort MCP CS grind; introduce plugin as bulk transport.
3. Fixed `defaultVariantId` → use `defaultVariant.id`.
4. Normalizer: exclude Icons-page from standalone components.
5. Validator: mapping collisions demoted to warnings for Snapshot v1 freeze.

## Architecture doc

See `docs/snapshot-architecture.md` (Snapshot Architecture v1 frozen).

## Sprint 02 readiness

- Diff consecutive Figma exports against Git history hashes
- Resolve or formally accept mapping-collision policy
- Optional: install `jsonschema` in CI for formal schema gate
- Targeted MCP known-check automation against canonical snapshot
- Preview / structural-audit layers (deferred)
