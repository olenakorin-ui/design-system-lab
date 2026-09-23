# Experiment: Access Request Review v0.1

**Design System baseline:** `v0.1.0` (`1e259a9`)  
**Branch:** `experiment/access-request-review-v0.1`  
**Question:** Can Cursor build a realistic B2B/admin workflow using DS v0.1.0 without inventing components, colors, tokens, or interaction patterns?

## Timing

| | |
|---|---|
| **START TIME** | 2026-09-23T10:30:20Z |
| **END TIME** | 2026-09-23T10:32:16Z |
| **IMPLEMENTATION DURATION** | ~2 minutes (single implementation pass after scaffold) |
| **PROMPT ITERATIONS** | 1 |

## Existing components reused (8/8)

| Component | Usage |
|---|---|
| Button | Back, Reject, Approve, Retry, dialog actions, harness |
| Input | Reference ticket |
| Checkbox | Review confirmation |
| Badge | Status (Pending/Approved/Rejected), Viewer, permission chips |
| Select | Access level |
| Alert | Risk callout, success/reject feedback, load error |
| Tabs | Overview / Permissions / Activity |
| Dialog | Approve + Reject confirmations |

**Duplicate DS components:** 0

## New components required

None as design-system primitives. Prototype-only:

- `AccessRequestReview` screen composition
- `trackAccessRequest` analytics stub

## Token violations

**0** — layout uses semantic utilities (`bg-background`, `text-foreground`, `border-border`, `text-muted-foreground`, `font-mono` for permission keys). No product hex.

## Hardcoded color violations

**0** — Dialog overlay still uses DS Dialog’s existing `bg-black/80` (known DS gap from v0.1.0; not introduced here).

## Invented semantic tokens

**0**

## Accessibility issues

| Issue | Severity | Notes |
|---|---|---|
| None critical | — | Labels via `htmlFor`; Dialogs use Radix focus trap; Checkbox/Select/Input disabled semantics in Viewer/read-only |
| Escape on dialog | Pass | Radix |
| Keyboard to Approve/Reject | Pass | Native buttons; gated until confirmation checked |

**Critical accessibility issues:** 0

## Figma / DS inconsistencies

- Status “Pending / Approved” have no dedicated Figma status Badge variants in v0.1.0; mapped to `secondary` / `verified` / `destructive`.
- No Toast in DS — success/reject use Alert (per experiment rules).

## Manual corrections

1. Avoided firing `decision_cancelled` on successful dialog close (only Cancel button).
2. Status badge mapping documented as DS gap (no success/pending semantics).

## DS GAPS

### DS GAP 1 — Product status lifecycle mapping

- **Need:** Distinct Pending / Approved (success) badge or status tokens  
- **Reason:** Product vocabulary uses Pending/Approved/Rejected; Badge only has default/secondary/outline/destructive/verified  
- **Existing alternatives:** `secondary` (Pending), `verified` (Approved), `destructive` (Rejected)  
- **Recommendation:** Add Figma Mode status tokens + Badge variants when product prioritizes status color meaning — **do not invent now**

### DS GAP 2 — Dialog overlay/scrim semantic

- **Need:** Semantic overlay/scrim token  
- **Reason:** Already known in Dialog parity (`black/80`)  
- **Existing alternatives:** Current Dialog overlay  
- **Recommendation:** Add Mode overlay token in a future DS release

### DS GAP 3 — Optional Label/FormField composition pattern

- **Need:** Optional Label/FormField composite  
- **Reason:** Labels composed with native `<label>` (acceptable)  
- **Existing alternatives:** Native label + Input/Select APIs (as in component stories)  
- **Recommendation:** Optional later; not blocking

## Analytics events (documented + stubbed)

| Event | When |
|---|---|
| `access_request_viewed` | Screen mount / retry |
| `access_request_tab_changed` | Tabs change |
| `access_level_changed` | Select change |
| `review_confirmation_checked` | Checkbox toggle |
| `decision_started` | Open Approve/Reject dialog |
| `decision_cancelled` | Cancel in dialog |
| `request_approved` | Confirm approve |
| `request_rejected` | Confirm reject |

## Build result

| Command | Result |
|---|---|
| `npm run build` | Pass |
| `npm run build-storybook` | Pass |

## Success guardrails

| Guardrail | Result |
|---|---|
| Existing intended components reused | **8/8** |
| Hardcoded product colors | **0** |
| Invented semantic tokens | **0** |
| Duplicate DS components | **0** |
| Critical accessibility issues | **0** |
| Build failures | **0** |
| Prompt iterations | **1** |

## Validation checklist

- [x] Light / Dark (Storybook toolbar + DarkMode story; App uses semantic surfaces)
- [x] Pending / Approved / Rejected
- [x] Viewer read-only
- [x] Error + Retry
- [x] Keyboard / Dialog focus (Radix)
- [x] Long names
- [x] Narrow viewport story

## Files

- `src/prototypes/access-request-review/AccessRequestReview.tsx`
- `src/prototypes/access-request-review/AccessRequestReview.stories.tsx`
- `src/prototypes/access-request-review/analytics.ts`
- `src/App.tsx` (experiment harness)
- `docs/experiments/access-request-review-v0.1.md`
