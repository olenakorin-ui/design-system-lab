# Experiment: User Access Management v0.2 — Content states migration

**Design System baseline:** `main` (Sprint 2 Empty State / Skeleton / Pagination available)  
**Branch:** `prototype/user-access-management-v0.2-states`  
**Route:** `/prototypes/user-access-management`  
**Question:** Do Empty State, Skeleton, and Pagination replace Alert / full-list workarounds without redesigning UAM or inventing DS APIs?

## Timing

| | |
|---|---|
| **START TIME** | 2026-09-25T11:22:00Z |
| **END TIME** | 2026-09-25T11:35:00Z |
| **PROMPT ITERATIONS** | **1** |

## Before vs after

| Dimension | Before | After |
|---|---|---|
| Loading | Alert | Table-shaped `Skeleton` + `aria-busy` |
| Empty directory | Alert | EmptyState — Invite user |
| Search/filter empty | Alert | EmptyState — Clear filters |
| Large dataset | Full filtered list | Client-side Pagination (page size 5) |
| Table / Menu / selection | Present | Preserved; select-all = **current page** |

## Selection behavior

- Selection **persists across pages** (`selectedIds`).
- **Select all** toggles only visible rows on the **current page**.
- Bulk bar shows the **global** selected count (e.g. page1:2 + page2:1 → **3 selected**).

## Filter / page reset

When search, role, status, or tab changes the result set, page resets to **1** (after scenario seed). If `totalPages` shrinks, current page is clamped so an empty page cannot result from stale pagination alone.

## Measurement

| Metric | Result |
|---|---|
| **ALERT MISUSE** | Loading/empty no longer Alert; Alert remains for **error** + action feedback |
| **EMPTY-STATE WORKAROUNDS** | Removed |
| **LOADING WORKAROUNDS** | Removed |
| **FULL-LIST WORKAROUND** | Removed when > page size |
| **DS COMPONENTS REUSED** | EmptyState, Skeleton, Pagination (+ Table, Menu, Checkbox, …) |
| **PRODUCT-SPECIFIC CODE** | Page size, windowing, skeleton row layout, empty copy |
| **TOKEN VIOLATIONS** | **0** |
| **HARDCODED COLORS** | **0** |
| **A11Y ISSUES** | **0** critical |
| **MANUAL CORRECTIONS** | SPA page-seed vs filter reset via skip ref; `empty` = `users: []` |
| **PROMPT ITERATIONS** | **1** |
| **BUILD FAILURES** | **0** |

## Product analytics (prototype docs — not Vercel custom events)

| Event | When |
|---|---|
| `user_directory_page_changed` | Pagination previous / next / page link |
| `user_directory_empty_action_clicked` | Empty CTA Invite / Clear filters |
| `user_directory_filters_cleared` | Clear filters recovery |

Hobby Web Analytics does **not** receive these as Vercel custom events.

## Qualitative assessment

| Aspect | Assessment |
|---|---|
| State clarity | Distinct loading / no-data / no-results / error |
| Loading quality | Skeleton approximates table |
| Empty recovery | Invite vs Clear filters |
| Pagination discoverability | Controls under table when multi-page |
| Selection clarity | Documented page-scoped select-all + cross-page persistence |
| Responsive | D009 scroll; EmptyState action stack |

## Scenarios

default · search · filtered · empty · search-no-results · loading · error · selected · multi · multi-page-selection · page-first · page-middle · page-last · viewer · long

## Remaining DS gaps

Status semantics · Overlay/scrim · FormField · Figma Checkbox Indeterminate · stacked mobile table (D009)

## Answer

**Yes** for content-state migration. Ready for Preview validation; do not merge until hosted QA.
