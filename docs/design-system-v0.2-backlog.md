# Design System v0.2 backlog

Evidence-driven backlog from Product Usage Experiments 01–02.  
Sprint 1: `ds/v0.2-data-foundation` (merged).  
Sprint 2: `ds/v0.2-content-states`.

Source experiments:

- Experiment 01 — Access Request Review (`docs/experiments/access-request-review-v0.1.md`)
- Experiment 02 — User Access Management (`docs/experiments/user-access-management-v0.1.md`)
- Migration — UAM v0.2 (`docs/experiments/user-access-management-v0.2-migration.md`) **validated**

**Status legend:** Validated · In progress · Research · Debt · Deferred

---

## Validated (Sprint 1)

### Checkbox Indeterminate — **Validated** (code); Figma follow-up pending

### Table foundation — **Validated**

### Dropdown Menu — **Validated**

---

## In progress (Sprint 2)

### Empty State — **In progress**

| | |
|---|---|
| **Need** | Non-error empty content (replace Alert-as-empty) |
| **Evidence** | Exp 01/02 empty workarounds |
| **Implementation** | `empty-state.tsx`; docs/components/empty-state.md |
| **Figma** | Pro Blocks / Empty Content `11002:8898` |

### Skeleton — **In progress**

| | |
|---|---|
| **Need** | Loading placeholder primitive |
| **Evidence** | Exp 02 loading via Alert |
| **Implementation** | `skeleton.tsx`; docs/components/skeleton.md |
| **Figma** | Skeleton `295:462` |

### Pagination — **In progress**

| | |
|---|---|
| **Need** | Paged dataset navigation chrome |
| **Evidence** | Exp 02 full-list workaround |
| **Implementation** | `pagination.tsx`; docs/components/pagination.md |
| **Figma** | Pagination `208:1701` + PaginationItem |

---

## Research

### Status semantic model — Research

### Field / FormField pattern — Research

---

## Debt

### Overlay / Scrim semantic — Debt

| | |
|---|---|
| **Current workaround** | `bg-black/80` on Dialog |
| **Dependencies** | Figma Mode overlay token |

### Figma Checkbox Indeterminate — Debt

| | |
|---|---|
| **Code** | Validated (`checked="indeterminate"`) |
| **Figma** | Add Status=Indeterminate to Checkbox axis |

---

## Deferred

### Stacked mobile data layout pattern — Deferred (**D009**)

---

## Out of scope until approved

Avatar · Combobox · Toast · inventing status tokens without Figma · DataGrid features · changing existing component APIs solely for prototypes · automatic column hiding · duplicate mobile table markup · product-specific Skeleton/Empty compounds
