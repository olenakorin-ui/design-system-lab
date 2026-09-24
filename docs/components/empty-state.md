# Empty State — Figma ↔ code parity (v0.2)

Figma: [Pro Blocks / Empty Content `11002:8898`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=11002-8898)  
Code: `src/components/ui/empty-state.tsx`  
Stories: `src/components/ui/empty-state.stories.tsx`

## Scope

Reusable **non-error** empty-content pattern. No product-specific copy in the API.

## API

| Export | Role |
|---|---|
| `EmptyState` | Dashed bordered container |
| `EmptyStateIcon` | Optional icon chrome (decorative icons: `aria-hidden`) |
| `EmptyStateHeader` | Title + description stack |
| `EmptyStateTitle` | `<h2>` |
| `EmptyStateDescription` | Supporting text |
| `EmptyStateActions` | Optional action slot (compose existing `Button`) |

## Figma → code

| Figma | Code |
|---|---|
| Dashed border card | `border-dashed border-border rounded-lg p-6` |
| Icon wrapper | `EmptyStateIcon` — `bg-card border-border shadow-xs` |
| Title | `text-xl font-semibold text-foreground` |
| Description | `text-sm text-muted-foreground` |
| Primary / Outline buttons | Consumer `Button` in `EmptyStateActions` |
| Desktop row / mobile stack actions | `flex-col sm:flex-row` |

## Stories

Default, WithAction, SearchNoResults, WithoutIcon, LongContent, DarkMode

## Accessibility

Meaningful heading (`EmptyStateTitle`); description as text; decorative icons `aria-hidden`; actions are normal `Button`s (keyboard + focus inherited).

## Known differences

1. Figma lives under **Pro Blocks**, not a standalone “Empty State” page — code names the reusable pattern `EmptyState`.
2. Product copy (e.g. “No databases added”) stays in stories/consumers only.
3. Dual CTA fully optional via composition.
