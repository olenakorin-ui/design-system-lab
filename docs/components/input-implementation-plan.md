# IMPLEMENTATION PLAN — Input v0.1

Figma source: [Input `65:533`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=65-533)

## Scope (this sprint)

Implement the **native text field control** (shadcn/Input pattern) that matches Figma’s inner `Input` chrome — not the full composite (label / description / link / horizontal layout / File chrome).

## Screens

- Storybook only. Light/Dark via toolbar + dedicated DarkMode story.

## Components

- `Input` (`src/components/ui/input.tsx`)

## States

| Concern | Ownership |
|---|---|
| Default / Focus / Filled | CSS + native value |
| Disabled | React `disabled` |
| Error / Error (Focus) | React `invalid` + CSS `:focus-visible` |
| Hover | none specified distinctly in Figma field chrome |

## Interactions

- Native `<input>` keyboard, caret, selection.
- Focus-visible: border `ring` + 3px `custom/outline`; when `invalid`, border `destructive` + 3px `custom/destructive-20-dark-40`.

## Data assumptions

- Stories use static values; no form library.

## Technical assumptions

- Semantic/custom tokens only (`input`, `ring`, `foreground`, `muted-foreground`, `destructive`, custom background/outline/destructive recipes).
- `invalid` maps Figma State=Error / Error (Focus); sets `aria-invalid`.
- Label / `aria-describedby` composed in stories (not built into Input).

## Out of scope (document as known differences)

- Figma Variant=File composite chrome
- Horizontal Layout / Label / Description / Link boolean props
- Leading icon slot (optional in Figma)

## Unresolved UX questions

None blocking for the control-only API.
