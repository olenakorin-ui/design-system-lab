# Experiment: User Access Management v0.1

**Design System baseline:** `v0.1.0` (current `main`)  
**Branch:** `prototype/user-access-management`  
**Question:** Can DS v0.1 support a realistic data-dense B2B/admin workflow without inventing components, tokens, colors, or interaction patterns?

## Timing

| | |
|---|---|
| **START TIME** | 2026-09-23T12:39:00Z |
| **END TIME** | 2026-09-23T12:41:04Z |
| **IMPLEMENTATION DURATION** | ~2 minutes (single pass) |
| **PROMPT ITERATIONS** | 1 |

## Existing components reused (8/8 intended)

| Component | Usage |
|---|---|
| Button | Invite, bulk, row actions, Retry, scenario harness, dialogs |
| Input | Search, invite email |
| Checkbox | Row select, select-all |
| Badge | Status + Viewer |
| Select | Role + status filters |
| Alert | Loading, empty, error, success feedback |
| Tabs | All users / Needs attention |
| Dialog | Invite, bulk deactivate, row deactivate |

**Duplicate DS components:** 0

## New components required

None as DS primitives. Prototype-only:

- `UserAccessManagement` screen composition (list rows, not a Table primitive)
- `trackUam` analytics stub

## DS GAPS

### DS GAP 1 — Data table / dense directory

- **Need:** Table (or equivalent dense grid) with sticky header, column alignment  
- **Why:** Admin directories expect scannable columns across many rows  
- **Current alternatives:** Stacked list rows with `dl` fields + border; works but not tabular  
- **Impact:** Density and compare-across-rows weaker than a table  
- **Recommendation:** Evaluate Table in a future DS release — **not invented here**

### DS GAP 2 — Row overflow actions (Dropdown Menu)

- **Need:** Dropdown Menu for multiple row actions  
- **Why:** More than one row action crowds the row on narrow viewports  
- **Current alternatives:** Single primary `Button` (“Deactivate”) + Dialog  
- **Impact:** Limited action vocabulary per row  
- **Recommendation:** Add Dropdown Menu when multi-action rows are common

### DS GAP 3 — Loading skeleton

- **Need:** Skeleton for list loading  
- **Why:** Alert “Loading…” is functional but not density-faithful  
- **Current alternatives:** Alert + disabled controls  
- **Impact:** Weaker loading affordance  
- **Recommendation:** Skeleton later if product prioritizes perceived performance

### DS GAP 4 — Empty state pattern

- **Need:** Dedicated Empty State  
- **Why:** Empty results are a first-class directory state  
- **Current alternatives:** Alert “No users found”  
- **Impact:** Acceptable for experiment; not a reusable empty pattern  
- **Recommendation:** Optional Empty State composite later

### DS GAP 5 — Status lifecycle semantics

- **Need:** Status tokens/variants for Active / Inactive / Suspended / Invited  
- **Why:** Mapped to `verified` / `outline` / `destructive` / `secondary`  
- **Current alternatives:** Existing Badge variants only  
- **Impact:** Color meaning is approximate (same class as Experiment 01)  
- **Recommendation:** Figma Mode status tokens before inventing

### DS GAP 6 — Pagination

- **Need:** Pagination for large directories  
- **Why:** 12 mocks fit one screen; real orgs need paging  
- **Current alternatives:** Full filtered list render  
- **Impact:** Fine for prototype density stress; not production-scale  
- **Recommendation:** Pagination when lists exceed ~page size

## Token violations

**0**

## Hardcoded color violations

**0** (product UI). Dialog overlay remains existing DS `black/80`.

## Invented semantic tokens

**0**

## Accessibility issues

| Issue | Severity | Notes |
|---|---|---|
| Indeterminate select-all icon | Low | Radix supports indeterminate; indicator still shows Check glyph only |
| None critical | — | Labels, Dialog focus trap, disabled Viewer semantics |

**Critical accessibility issues:** 0

## Manual corrections

1. Removed duplicate `disabled` prop on search Input during implementation.
2. Used Alert for loading/empty instead of inventing Skeleton/Empty State.
3. Row actions as Button + Dialog (no Dropdown Menu).

## Prototype-specific patterns

- Scenario query (`?scenario=`) drives initial filters/selection/load state
- Stacked list rows instead of Table
- Bulk bar appears only when selection > 0 (existing Button)

## Build result

| Command | Result |
|---|---|
| `npm run build` | Pass |
| `npm run build-storybook` | Pass |

## Success guardrails

| Guardrail | Result |
|---|---|
| Intended components reused | **8/8** |
| Hardcoded product colors | **0** |
| Invented semantic tokens | **0** |
| Duplicate DS components | **0** |
| Critical a11y issues | **0** |
| Build failures | **0** |
| Prompt iterations | **1** |
| Disallowed DS primitives added | **0** (Table/Menu/Pagination/Skeleton/Empty/Avatar/Combobox not added) |
