# Design System v0.2 backlog

Evidence-driven backlog from Product Usage Experiments 01–02.  
Sprint 1 branch: `ds/v0.2-data-foundation`.

Source experiments:

- Experiment 01 — Access Request Review (`docs/experiments/access-request-review-v0.1.md`)
- Experiment 02 — User Access Management (`docs/experiments/user-access-management-v0.1.md`)

**Status legend:** Validated · In progress · Deferred

---

## EVIDENCE

### Experiment 01 — Access Request Review

- Form/admin decision flow on DS v0.1 succeeded with 8/8 intended components.
- Gaps: status lifecycle mapping; Dialog overlay/scrim; optional Label/FormField.

### Experiment 02 — User Access Management

- Data-dense directory on DS v0.1 succeeded without inventing primitives (stacked rows).
- Gaps: Table; Dropdown Menu; Skeleton; Empty State; status semantics; Pagination; Checkbox indeterminate visual.
- Inherited: Dialog overlay/scrim.

---

## Validated (Sprint 1)

### Checkbox Indeterminate — **Validated** (code); Figma follow-up pending

| | |
|---|---|
| **Need** | Distinct indeterminate indicator for select-all |
| **Evidence** | Exp 02 multi-select |
| **Implementation** | `checked="indeterminate"` + Minus icon; docs/components/checkbox.md |
| **Figma** | Status axis still Active/Inactive only — add **Indeterminate** |
| **API** | No new React prop — Radix `checked` model |

### Table foundation — **Validated**

| | |
|---|---|
| **Need** | Dense multi-column data display |
| **Evidence** | Exp 02 directory |
| **Implementation** | Semantic table primitives; docs/components/table.md |
| **Responsive** | **D009** — wide = native table; narrow = horizontal scroll |
| **Remaining** | Data Table filters/sort/pagination deferred |

### Dropdown Menu — **Validated**

| | |
|---|---|
| **Need** | Overflow / multi row actions |
| **Evidence** | Exp 02 row actions |
| **Implementation** | Radix menu composition; docs/components/dropdown-menu.md |
| **Remaining** | Avatar trigger / User item when Avatar ships |

---

## Deferred

### Stacked mobile data layout pattern — **Deferred**

| | |
|---|---|
| **Need** | Card-like / stacked rows on narrow viewports |
| **Why deferred** | Not part of base Table; would break the global rule (native table + horizontal scroll) |
| **Rule** | Do not add `responsive="cards"` (or equivalent) to core Table API in v0.2 |
| **Next** | Separate pattern/component investigation if prototype evidence requires it |

### Overlay / Scrim semantic — **Deferred**

| | |
|---|---|
| **Need** | Mode semantic for Dialog overlay |
| **Evidence** | Exp 01 + Exp 02 |
| **Current workaround** | `bg-black/80` |
| **Dependencies** | Figma Mode overlay token |

### Empty State — Deferred

### Skeleton — Deferred

### Pagination — Deferred

### Status semantic model — Deferred

### Field / FormField pattern — Deferred

---

## Out of scope until approved

Avatar · Combobox · Toast · inventing status tokens without Figma · DataGrid features · changing existing component APIs solely for prototypes · automatic column hiding · duplicate mobile table markup
