# Access Request Review

Admin workflow prototype for reviewing elevated system access.

| | |
|---|---|
| **Status** | Validated (Experiment 01) |
| **Design System** | v0.1.0 |
| **Primary runtime** | Prototype Lab — `/prototypes/access-request` |
| **Storybook** | Regression only (`Prototypes/Access Request Review (regression)`) |

## Scenarios

Query: `?scenario=<id>`

| Scenario | Behavior |
|---|---|
| `pending` (default) | Reviewer can confirm and approve/reject |
| `approved` | Terminal approved state, read-only decisions |
| `rejected` | Terminal rejected state, read-only decisions |
| `viewer` | Read-only role; no approve/reject or field edits |
| `error` | Load error + Retry |

## Structure

```text
access-request-review/
  README.md
  analytics.ts
  AccessRequestReview.stories.tsx   # regression
  components/AccessRequestReview.tsx
  pages/AccessRequestPage.tsx
  mocks/scenarios.ts
  state/types.ts
```
