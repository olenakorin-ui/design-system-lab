# User Access Management

Admin directory workflow: search, filter, select, and act on users.

| | |
|---|---|
| **Status** | Migration validation (v0.2) |
| **Design System** | v0.2 data foundation (Table, Dropdown Menu, Checkbox indeterminate) |
| **Primary runtime** | Prototype Lab — `/prototypes/user-access-management` |
| **Branch** | `prototype/user-access-management-v0.2` |
| **Experiment log** | `docs/experiments/user-access-management-v0.2-migration.md` |
| **Storybook** | Not primary (no dedicated story required) |

## Scenarios

`?scenario=<id>`

default · search · filtered · empty · loading · error · selected · multi · viewer · long

## Structure

```text
user-access-management/
  README.md
  analytics.ts
  components/UserAccessManagement.tsx
  pages/UserAccessManagementPage.tsx
  mocks/users.ts
  mocks/scenarios.ts
  state/types.ts
```
