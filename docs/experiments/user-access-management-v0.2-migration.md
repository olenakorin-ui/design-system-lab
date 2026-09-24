# Experiment: User Access Management v0.2 — Migration validation

**Design System baseline:** `main` after DS v0.2 Sprint 1 (`ds/v0.2-data-foundation` merged)  
**Branch:** `prototype/user-access-management-v0.2`  
**Preview:** https://design-system-lab-git-prototype-user-access-manag-3e801d-okorin.vercel.app  
**Deployment:** https://design-system-x1u9htv6y-okorin.vercel.app (**Ready**)  
**Route:** `/prototypes/user-access-management` (same route; migrated implementation)  
**Question:** Does migrating Exp 02 from v0.1 workarounds to validated Table / Dropdown Menu / Checkbox indeterminate improve density UX without inventing new DS APIs?

## Timing

| | |
|---|---|
| **START TIME** | 2026-09-24T11:43:00Z |
| **END TIME** | 2026-09-24T11:48:00Z |
| **IMPLEMENTATION DURATION** | ~5 minutes (single pass after merge) |
| **PROMPT ITERATIONS** | **1** |

## Before vs after

| Dimension | v0.1 | v0.2 migration |
|---|---|---|
| Directory layout | Stacked `<ul>` / card-like rows | DS `Table` primitives |
| Row actions | Single `Button` → Dialog | `DropdownMenu` (View / Edit access / Deactivate) → Dialog for destructive |
| Select-all partial | `checked="indeterminate"` a11y OK; visual was Check-only | Minus indeterminate indicator (Sprint 1) |
| Narrow viewport | Stacked rows | Horizontal scroll (**D009**) |
| Empty / loading | Alert workarounds | Unchanged (Empty / Skeleton still deferred) |
| Status | Badge variant mapping | Unchanged (no status semantics) |

## Measurement

| Metric | Result |
|---|---|
| **CUSTOM ROW MARKUP** | Removed stacked `<li>` cards; replaced with semantic table cells |
| **PRODUCT-SPECIFIC WORKAROUNDS** | Empty→Alert, Loading→Alert, Badge status map remain |
| **DS COMPONENTS REUSED** | Table, Dropdown Menu, Checkbox (+ prior Button, Input, Badge, Select, Alert, Tabs, Dialog) |
| **SELECTION LOGIC** | Unchanged: per-row, select-all, clear, bulk bar; header Checkbox uses `indeterminate` |
| **ROW ACTION LOGIC** | Menu items; Deactivate still opens existing Dialog |
| **A11Y ISSUES** | **0** critical introduced; labelled checkboxes; menu trigger `aria-label`; caption `sr-only` |
| **MANUAL CORRECTIONS** | `icon-sm` avoided (use `size="icon"`); truncate + `title` on long emails |
| **PROMPT ITERATIONS** | **1** |
| **BUILD FAILURES** | **0** |
| **RESPONSIVE COMPLEXITY** | Low — Table container `overflow-x-auto` only; no card conversion |

## Qualitative assessment

| Aspect | Assessment |
|---|---|
| Scanability | Improved — aligned columns vs stacked cards |
| Column alignment | Native table headers associate fields |
| Selection clarity | Header + row checkboxes; indeterminate Minus visible |
| Action discoverability | Overflow menu groups View / Edit / Deactivate |

## Validation checklist

| Scenario | Expected |
|---|---|
| default | Table lists mock users |
| search / filtered | Same filter logic; table updates |
| selected / multi-select | Row `data-state=selected`; bulk bar |
| partial select-all | Header Checkbox `indeterminate` |
| viewer | Invite, checkboxes, menu disabled |
| long content | Truncate email + horizontal scroll |
| Light / Dark | Semantic tokens only |
| narrow viewport | Horizontal scroll, no stacked cards |

## Remaining DS gaps (unchanged / deferred)

1. Empty State  
2. Skeleton  
3. Pagination  
4. Status semantic model  
5. Overlay / scrim token  
6. Figma Checkbox Status=Indeterminate (code validated)  
7. Stacked mobile data layout pattern (explicitly **not** Table — D009)

## Answer

**Yes:** Exp 02 migrates cleanly onto Sprint 1 data foundation. Density and action discoverability improve without new tokens, status semantics, or core DS APIs.
