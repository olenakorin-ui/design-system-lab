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

## P0

### Checkbox indeterminate visual state — **Validated** (Sprint 1)

| | |
|---|---|
| **Need** | Distinct indeterminate indicator for select-all |
| **Evidence** | Exp 02 multi-select |
| **Implementation** | `checked="indeterminate"` + Minus icon; docs/components/checkbox.md |
| **Remaining** | Add Figma Status=Indeterminate for full design ownership |

### Table — **Validated** (Sprint 1 foundation)

| | |
|---|---|
| **Need** | Dense multi-column data display |
| **Evidence** | Exp 02 directory |
| **Implementation** | Semantic table primitives; docs/components/table.md |
| **Remaining** | Responsive stacked vs scroll (**DECISION REQUIRED**); Data Table filters/sort/pagination deferred |

### Dropdown Menu — **Validated** (Sprint 1)

| | |
|---|---|
| **Need** | Overflow / multi row actions |
| **Evidence** | Exp 02 row actions |
| **Implementation** | Radix menu composition; docs/components/dropdown-menu.md |
| **Remaining** | Avatar trigger / User item when Avatar ships |

### Overlay / Scrim semantic — **Deferred**

| | |
|---|---|
| **Need** | Mode semantic for Dialog overlay |
| **Evidence** | Exp 01 + Exp 02 |
| **Current workaround** | `bg-black/80` |
| **Why DS-level** | Token architecture |
| **Dependencies** | Figma Mode overlay token |
| **Proposed validation** | Dialog Light/Dark contrast |

---

## P1 — **Deferred** (not Sprint 1)

### Empty State — Deferred

### Skeleton — Deferred

### Pagination — Deferred

---

## RESEARCH / DECISION — **Deferred**

### Status semantic model — Deferred

### Field / FormField pattern — Deferred

---

## Out of scope until approved

Avatar · Combobox · Toast · inventing status tokens without Figma · DataGrid features · changing existing component APIs solely for prototypes
