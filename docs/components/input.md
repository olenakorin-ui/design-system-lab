# Input — Figma ↔ code parity

Figma: [Input `65:533`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=65-533)  
Code: `src/components/ui/input.tsx`  
Stories: `src/components/ui/input.stories.tsx`

## API (application state)

| Prop | Type | Notes |
|---|---|---|
| native input attrs | — | `type`, `name`, `value`, `defaultValue`, `placeholder`, `required`, `readOnly`, `disabled`, `id`, `aria-*`, … |
| `invalid` | `boolean` | Maps Figma State=Error / Error (Focus); sets `aria-invalid` |

**Not props (CSS / native):** hover, focus-visible, filled (value presence).

Label, description, and `aria-describedby` are composed by the consumer (demonstrated in stories). Placeholder must not replace a visible label.

## Figma → code mapping

| Figma | Code |
|---|---|
| Inner field Default | `border-input`, `bg-[var(--custom-background-dark-input-30)]`, `h-9`, `px-3`, `rounded-md`, `shadow-xs` |
| Placeholder text | `placeholder:text-muted-foreground` |
| Filled text | `text-foreground` (native value) |
| State=Focus | `:focus-visible` → `border-ring` + 3px `--custom-outline` |
| State=Disabled | `disabled` → `opacity-50` |
| State=Error | `invalid` → `aria-invalid` + `border-destructive` |
| State=Error (Focus) | `invalid` + `:focus-visible` → destructive border + 3px `--custom-destructive-20-dark-40` |
| Variant=File | Native `type="file"` + `file:` utilities (not full Figma File chrome) |

## Token usage

- `--custom-background-dark-input-30`, `--input`, `--ring`, `--foreground`, `--muted-foreground`, `--destructive`
- Focus: `--custom-outline`; invalid focus: `--custom-destructive-20-dark-40`
- `--radius-md`, `--shadow-xs`, `--font-sans`

No hardcoded product colors. No invented status tokens (`success` / `warning` / `info`).

## Storybook coverage

Default, WithValue, Placeholder, Disabled, Invalid, FocusVisible, LongValue, DarkMode

## Accessibility results

| Check | Result |
|---|---|
| Native `<input>` | Yes |
| Label association | Stories use `<label htmlFor>` |
| `aria-invalid` | Set when `invalid` |
| `aria-describedby` | Stories wire description id |
| Focus visibility | 3px outline / destructive recipe |
| Placeholder ≠ label | Visible label required in stories |

## Visual parity results

Field chrome (height, radius, border, fill, focus/error rings, disabled opacity) matches Figma Default Variant field. Light/Dark Mode recipes apply via `.dark`.

## Known differences

1. **Composite out of scope** — Figma includes Label, Description, Link, Horizontal Layout, and File “Choose file” chrome as one component set. Code ships the **field control** only; composition is the consumer’s job (shown in stories).
2. **Leading icon** — Figma optional `Show Icon`; not part of Input API yet (compose outside or follow up).
3. **Geist** — deferred (system fallback).
4. **Opacity** — uses Tailwind `opacity-50` matching Figma layer 0.5 (same pattern as Button).
