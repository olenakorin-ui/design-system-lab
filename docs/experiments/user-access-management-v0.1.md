# Experiment: User Access Management v0.1 — Final

**Design System baseline:** `v0.1.0` (from `main` at experiment start)  
**Branch:** `prototype/user-access-management`  
**Preview:** https://design-system-lab-git-prototype-user-access-management-okorin.vercel.app  
**Question:** Can DS v0.1 support a realistic data-dense B2B/admin workflow without inventing components, tokens, colors, or interaction patterns?

## Timing

| | |
|---|---|
| **START TIME** | 2026-09-23T12:39:00Z |
| **END TIME** | 2026-09-23T12:41:04Z |
| **IMPLEMENTATION DURATION** | ~2 minutes (single pass) |
| **PROMPT ITERATIONS** | **1** |
| **HOSTED QA** | 2026-09-23 (finalize) |

## Final metrics

| Guardrail | Result |
|---|---|
| Existing components reused | **8/8** |
| Hardcoded product colors | **0** |
| Invented semantics | **0** |
| Duplicate DS components | **0** |
| Critical accessibility issues | **0** |
| Prompt iterations | **1** |
| Build failures | **0** |
| Disallowed DS primitives added | **0** |

## Existing components reused (8/8)

Button · Input · Checkbox · Badge · Select · Alert · Tabs · Dialog

## Confirmed DS gaps

1. **Table** — dense directory used stacked list rows  
2. **Dropdown Menu** — row actions limited to Button + Dialog  
3. **Skeleton** — loading via Alert  
4. **Empty State** — empty via Alert  
5. **Status semantic model** — Badge variant mapping only  
6. **Pagination** — full filtered list  
7. **Checkbox indeterminate visual state** — Radix `indeterminate` works in a11y tree; indicator still renders Check glyph only  

### Inherited DS debt

- **Dialog overlay/scrim semantic** — Dialog still uses `bg-black/80` (Experiment 01 / D007-adjacent debt)

Cross-experiment backlog: `docs/design-system-v0.2-backlog.md`

## Hosted QA results

| Check | Result |
|---|---|
| Vercel Preview deployment | **Ready** |
| Prototype Hub (branch build) | Pass — Access Request + UAM listed |
| `/prototypes/user-access-management` + scenarios | Pass (default, search, filtered, empty, loading, error, selected, multi, viewer, long) |
| Light / Dark | Pass |
| Narrow viewport | Pass (stacked rows/controls) |
| Direct deep-link refresh | Pass (SPA `index.html` fallback locally; `vercel.json` on deploy) |
| Assets (JS/CSS) | Pass — 200 |
| Critical a11y | Pass — 0 critical |
| Runtime console errors | None observed in QA session |
| External / incognito on Preview URL | **Blocked by Vercel Deployment Protection (SSO login)** — see note |

**Note:** Unauthenticated requests to the Preview alias redirect to Vercel login. Functional QA of Experiment 02 scenarios was completed against the same branch build via local `vite preview` (mirrors production SPA). Production (`main`) remains publicly reachable but does **not** include UAM until merge.

## Token / color compliance

**0** product hex · **0** invented semantics · Dialog overlay debt unchanged

## Accessibility

Critical **0**. Labels, Dialog focus trap, Viewer disables mutations. Gap #7 is non-critical visual polish for select-all.

## Manual corrections

1. Duplicate Input `disabled` removed during build  
2. Alert used for loading/empty (no Skeleton/Empty invent)  
3. Row/bulk actions via Button + Dialog (no Menu invent)

## Build result

| Command | Result |
|---|---|
| `npm run build` | Pass |
| `npm run build-storybook` | Pass |

## Answer

**Yes for MVP density:** DS v0.1 can support the workflow with composition + documented gaps. Table / Menu / Skeleton / Empty / status / Pagination / indeterminate visual remain **recommendations**, not implemented.
