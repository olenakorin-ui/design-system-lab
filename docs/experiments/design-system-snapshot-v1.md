# Experiment: Design System Snapshot V1

**Status:** In progress (plugin transport ready; full A/B hash pending Figma Desktop export)  
**Branch:** `ds/snapshot-v1`  
**Figma:** Design System V2 (`ZllxQplWi5QJcNeUHeY8T3`)

## Goal

Deterministic, versioned, machine-readable snapshot of Design System V2:

```text
raw export → normalize → validate → SHA-256 → latest/ + history/
```

## Experiment phases

### Phase A — Figma MCP bulk extraction (failed as primary transport)

**Hypothesis:** Figma MCP `use_figma` can return full inventories (variables, styles, component sets, icons) for a single raw export.

**Result:** **Rejected as primary transport.**

| Observation | Detail |
| --- | --- |
| MCP PAYLOAD LIMIT ENCOUNTERED | Responses truncate at approximately **20 KB** |
| Symptom | Mid-JSON / mid-TSV cutoffs; incomplete terminal objects |
| Mitigation attempted | Batched extraction, TSV, base64 slices, inventory-first, resumable manifests under `design-system/snapshots/_raw/batches/` |
| Outcome | Variables (760) + icons (1468) + text (309) + effect (34) inventories/details largely recoverable via batches; **component-set details (~405)** remain impractical via MCP (~80+ small calls, frequent truncation on large sets e.g. Button) |

**Metrics (MCP path — partial):**

| Metric | Value |
| --- | --- |
| TOTAL BATCHES (validated, variables+icons+text+effect+partial CS) | 8 + 15 + 8 + 4 + 2 ≈ **37+** |
| RETRIED / REDUCED-SIZE / TRUNCATED BATCHES | Multiple truncation rejections during CS/text b64 attempts; transport helpers added |
| MISSING IDS AFTER ASSEMBLY (CS) | **~398** component sets not detail-complete via MCP |
| CONFLICTING DUPLICATE IDS | **0** observed in completed categories |
| RAW EXTRACTION COMPLETENESS | **Incomplete** (assembly gate blocked) |
| ASSEMBLY RESULT | Not assembled as canonical (gate: `allComplete=false`) |

MCP inventories, batch manifests, and helper scripts are **retained** as fallback / audit / experiment evidence. Do not delete.

**Decision:** Stop remaining MCP component-set grind. Switch bulk transport to a **local read-only Figma plugin**.

### Phase B — Figma Plugin exporter v0.1 (current)

**Hypothesis:** Plugin API in Figma Desktop can scan the full file and download one complete `figma-snapshot.raw.json` without MCP size limits.

**Implementation:** `tools/figma-snapshot-plugin/`

| Item | Status |
| --- | --- |
| Read-only plugin (manifest + `code.js` + `ui.html`) | **Ready** |
| Inventory UI + progress + completeness gate | **Ready** |
| Download only when complete | **Ready** |
| `defaultVariant` → `defaultVariantId` (correct API) | **Ready** |
| Icons = page named `Icons` only | **Ready** |
| Repo ingest `scripts/ingest-figma-plugin-raw.py` | **Ready** |
| Normalize / validate reuse | **Ready** |
| Live A/B export from Design System V2 | **Pending** (requires Figma Desktop user run) |

## Reference inventory (Design System V2 live audit)

| Category | Reference count |
| --- | ---: |
| Variables | 760 |
| Variable collections | 4 |
| Component sets | 405 |
| Standalone components | 285 |
| Text styles | 309 |
| Effect styles | 34 |
| Icons page | 1468 |

These are **reference** values for delta reporting, not permanently hardcoded schema requirements.

## Plugin export metrics (fill after Desktop run)

| Metric | A | B |
| --- | --- | --- |
| Export duration | _TBD_ | _TBD_ |
| Raw file size | _TBD_ | _TBD_ |
| Canonical tree size | _TBD_ | _TBD_ |
| Snapshot hash | _TBD_ | _TBD_ |
| Inventory vs reference | _TBD_ | _TBD_ |

## Determinism (required)

After two exports of unchanged Figma:

```text
HASH A == HASH B
CANONICAL DIFF == 0
```

Status: **blocked on user plugin export A/B**.

## Manual corrections / prompt iterations

1. MCP → batched TSV/b64 (multiple helper scripts) — still truncated for large CS payloads.
2. Abort ~80+ remaining MCP CS detail calls per Sprint 01-C.
3. Introduce plugin as bulk transport; MCP demoted to targeted inspection.
4. Fixed `defaultVariantId` assumption → use `defaultVariant.id`.

## Architecture doc

See `docs/snapshot-architecture.md`.

## Next

1. Import plugin from `tools/figma-snapshot-plugin/manifest.json` in Figma Desktop.
2. Export A → ingest → normalize → validate → record hash.
3. Export B → same → confirm HASH A == HASH B.
4. Record durations and file sizes in this report.
