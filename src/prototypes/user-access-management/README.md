# User Access Management

Admin directory workflow: search, filter, select, paginate, and act on users.

| | |
|---|---|
| **Status** | Validated — Design System v0.2.0 |
| **Design System** | v0.2.0 (Table, Menu, Checkbox indeterminate, Empty State, Skeleton, Pagination) |
| **Primary runtime** | Prototype Lab — `/prototypes/user-access-management` |
| **Production** | https://design-system-lab-weld.vercel.app/prototypes/user-access-management |
| **Experiment log** | `docs/experiments/user-access-management-v0.2-states-migration.md` |

## Selection across pages

- Selection **persists** when changing pages.
- **Select all** applies to the **current page only**.
- Bulk actions use the full selected set (all pages).

## Scenarios

`?scenario=<id>`

default · search · filtered · empty · search-no-results · loading · error · selected · multi · multi-page-selection · page-first · page-middle · page-last · viewer · long

## Product analytics

See `analytics.ts` and the experiment doc. Events are prototype CustomEvents / console — **not** Vercel Hobby custom events.
