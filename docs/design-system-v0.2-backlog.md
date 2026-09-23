# Design System v0.2 backlog

Evidence-driven backlog from Product Usage Experiments 01–02.  
**Do not implement until prioritized and approved** (Figma + product decisions where required).

Source experiments:

- Experiment 01 — Access Request Review (`docs/experiments/access-request-review-v0.1.md`)
- Experiment 02 — User Access Management (`docs/experiments/user-access-management-v0.1.md`)

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

### Checkbox indeterminate visual state

| | |
|---|---|
| **Need** | Distinct indeterminate indicator for select-all (not identical to checked Check glyph) |
| **Evidence** | Exp 02 multi-select; a11y exposes `indeterminate`, visual still Check-only |
| **Current workaround** | Radix indeterminate state; users rely on “N selected” text |
| **Why DS-level** | Shared Checkbox contract for all multi-select patterns |
| **Dependencies** | Figma Checkbox indeterminate variant |
| **Proposed validation** | Storybook: unchecked / checked / indeterminate / disabled; UAM select-all regression |

### Table

| | |
|---|---|
| **Need** | Dense, scannable multi-column data display with selection column |
| **Evidence** | Exp 02 directory; stacked rows weaken column compare |
| **Current workaround** | Bordered list rows + `dl` field grid |
| **Why DS-level** | Recurs across admin directories; must use Mode tokens + a11y |
| **Dependencies** | Figma Table; selection + Badge cell recipes |
| **Proposed validation** | Storybook density + selection; UAM prototype swap without product hex |

### Dropdown Menu

| | |
|---|---|
| **Need** | Overflow / multi row actions without crowding the row |
| **Evidence** | Exp 02 single “Deactivate” Button; more actions won’t fit narrow |
| **Current workaround** | One Button + Dialog |
| **Why DS-level** | Shared action disclosure pattern (Radix Menu) |
| **Dependencies** | Figma Menu; keyboard + focus |
| **Proposed validation** | Storybook items/disabled/destructive; UAM row actions |

### Overlay / Scrim semantic

| | |
|---|---|
| **Need** | Mode semantic for Dialog/modal overlay (replace `bg-black/80`) |
| **Evidence** | Exp 01 + Exp 02 Dialog; inherited DS debt |
| **Current workaround** | Existing Dialog overlay hard-coded opacity black |
| **Why DS-level** | Token architecture; Light/Dark consistency |
| **Dependencies** | Figma Mode overlay token; Dialog token bind |
| **Proposed validation** | Dialog stories Light/Dark; contrast check |

---

## P1

### Empty State

| | |
|---|---|
| **Need** | Reusable empty results pattern (title, description, optional action) |
| **Evidence** | Exp 02 “No users found” via Alert |
| **Current workaround** | Alert |
| **Why DS-level** | Recurs in search/filter UIs; avoid ad-hoc Alert misuse |
| **Dependencies** | Figma Empty; composition with Button |
| **Proposed validation** | Storybook variants; UAM empty scenario |

### Skeleton

| | |
|---|---|
| **Need** | Loading placeholders for dense lists |
| **Evidence** | Exp 02 loading via Alert |
| **Current workaround** | Alert “Loading users…” + disabled controls |
| **Why DS-level** | Shared perceived-performance pattern |
| **Dependencies** | Figma Skeleton; motion/reduced-motion |
| **Proposed validation** | Storybook; UAM loading scenario |

### Pagination

| | |
|---|---|
| **Need** | Page through large directories |
| **Evidence** | Exp 02 full list of 12 mocks; won’t scale |
| **Current workaround** | Render all filtered rows |
| **Why DS-level** | Shared navigation + a11y for lists/tables |
| **Dependencies** | Figma Pagination; optionally Table |
| **Proposed validation** | Storybook; UAM with larger mock set |

---

## RESEARCH / DECISION

### Status semantic model

| | |
|---|---|
| **Need** | Meaningful Pending/Approved/Active/Inactive/Suspended/Invited (etc.) without inventing lab-only tokens |
| **Evidence** | Exp 01 status badges; Exp 02 user status badges; D004 Decision2=B |
| **Current workaround** | Map to `secondary` / `verified` / `destructive` / `outline` |
| **Why DS-level** | Cross-product meaning; Figma Mode ownership |
| **Dependencies** | Product + Figma Mode status tokens decision |
| **Proposed validation** | Gap report → Mode tokens → Badge variants → Exp 01/02 remaps |

### Field / FormField pattern

| | |
|---|---|
| **Need** | Optional Label + control + hint/error composition |
| **Evidence** | Exp 01 forms; Exp 02 search/filters use native `<label>` |
| **Current workaround** | Native label + Input/Select APIs |
| **Why DS-level** | Density + error association consistency |
| **Dependencies** | UX decision whether composite is required |
| **Proposed validation** | If approved: Storybook FormField; no API break to Input |

---

## Out of scope until approved

Avatar · Combobox · Toast · inventing status tokens without Figma · changing existing component APIs solely for prototypes
