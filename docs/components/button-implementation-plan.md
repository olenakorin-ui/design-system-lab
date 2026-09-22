# IMPLEMENTATION PLAN — Button v0.1

Figma source: [Button `37:931`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=37-931)

## Screens

- Storybook stories only (no product screen). Light + Dark via Storybook toolbar.

## Components

- `Button` (`src/components/ui/button.tsx`) — shadcn/Radix `Slot` + CVA.
- Supporting: `cn` util, token-backed Tailwind theme, Storybook preview chrome.

## States

| Concern | Ownership |
|---|---|
| Default / Hover / Focus-visible / Pressed (active) | CSS (`:hover`, `:focus-visible`, `:active`) |
| Disabled | React `disabled` (+ `aria-disabled`) |
| Loading | React `loading` (`aria-busy`, spinner, disables interaction) |
| Variants / sizes / icons | React props |

## Interactions

- Keyboard: native `<button>` focus + Enter/Space.
- Focus-visible: 3px `custom/outline` ring (Destructive uses `custom/destructive-20-dark-40`).
- Loading replaces leading icon slot with `LoaderCircle`; hides left/right icons.
- Icon-only (`size="icon"`): requires accessible name (`aria-label` / `aria-labelledby`).

## Data assumptions

- No remote data. Stories use static labels + Lucide icons.

## Technical assumptions

- Vite + React 19 + TypeScript + Tailwind v4 (`@tailwindcss/vite`).
- Theme = generated `src/styles/tokens.css` (Mode Light/Dark via `.dark`).
- Semantic colors via CSS vars (`--primary`, …); custom Mode recipes for Outline / Destructive / focus.
- shadcn conventions: `variant`, `size`, `asChild`, CVA, `Slot`.
- Do **not** invent status tokens; use existing Mode `base/*` + `custom/*` recipes.

## Unresolved UX questions

None blocking Button v0.1. Hover for Default uses Figma `primary` + `alpha/90` overlay; code approximates with stacked background / `color-mix` where needed — see parity doc for differences.

## Figma inventory (read-only)

- **Variants:** Default, Secondary, Destructive, Outline, Ghost, Link
- **Sizes:** default (36), sm (32), lg (40), icon (36×36)
- **States:** Default, Hover, Focus, Loading, Disabled, Pressed
- **Icons:** optional left/right (16px), gap 8; Loading → LoaderCircle only
- **Token bindings (Default):** `base/primary`, `base/primary-foreground`, hover + `alpha/90`, focus `custom/outline`, disabled/loading opacity 50, pressed opacity 60, shadow `shadow/xs`
