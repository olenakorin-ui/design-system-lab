# Design System v0.2 backlog

Evidence-driven backlog from Product Usage Experiments 01–02.  
Sprint 1: `ds/v0.2-data-foundation` (merged).  
Sprint 2: `ds/v0.2-content-states` (merged).  
**Release:** Design System **v0.2.0** — data foundation and content states.

Source experiments:

- Experiment 01 — Access Request Review (`docs/experiments/access-request-review-v0.1.md`)
- Experiment 02 — User Access Management (`docs/experiments/user-access-management-v0.1.md`)
- Migration — UAM v0.2 table/menu (`docs/experiments/user-access-management-v0.2-migration.md`) **validated**
- Migration — UAM v0.2 content states (`docs/experiments/user-access-management-v0.2-states-migration.md`) **validated**

**Status legend:** Validated · Research · Debt · Deferred

---

## Release notes — Design System v0.2.0

**Theme:** data-dense B2B/admin workflows

Ships the v0.2 data foundation and content-state primitives needed for directory-style admin flows (search, filter, select, paginate, empty/loading), without inventing status or overlay tokens.

### Included

| Area | Scope |
|---|---|
| Checkbox Indeterminate | `checked="indeterminate"` for page-scoped select-all |
| Table | Foundation + horizontal scroll on narrow viewports (**D009**) |
| Dropdown Menu | Row actions / overflow menus |
| Empty State | Non-error empty + no-results compositions |
| Skeleton | Loading placeholders for directory content |
| Pagination | Paged dataset navigation chrome |

### Validated in product usage

User Access Management v0.2 on Production (`/prototypes/user-access-management`): loading, empty, no-results, pagination edges, filter/search page reset, cross-page selection, current-page select-all, Viewer/read-only, Light/Dark.

### Not in v0.2.0

Status semantic model · Overlay/Scrim semantic · FormField · Figma Checkbox Indeterminate variant · stacked mobile table pattern (**D009** deferred)

---

## Validated (v0.2.0)

### Checkbox Indeterminate — **VALIDATED** (code); Figma follow-up pending

### Table — **VALIDATED**

### Dropdown Menu — **VALIDATED**

### Empty State — **VALIDATED**

### Skeleton — **VALIDATED**

### Pagination — **VALIDATED**

---

## Research (open)

### Status semantic model — Research

### Field / FormField pattern — Research

---

## Debt (open)

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

## Deferred (open)

### Stacked mobile data layout pattern — Deferred (**D009**)

---

## Out of scope until approved

Avatar · Combobox · Toast · inventing status tokens without Figma · DataGrid features · changing existing component APIs solely for prototypes · automatic column hiding · duplicate mobile table markup · product-specific Skeleton/Empty compounds
