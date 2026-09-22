# Checkbox — Figma ↔ code parity

Figma: [Checkbox `46:112`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=46-112)  
Code: `src/components/ui/checkbox.tsx`  
Stories: `src/components/ui/checkbox.stories.tsx`

## API (application state)

| Prop | Type | Notes |
|---|---|---|
| `checked` | `boolean` | Controlled; maps Figma Status=Active/Inactive |
| `defaultChecked` | `boolean` | Uncontrolled initial |
| `disabled` | `boolean` | Figma State=Disabled |
| `onCheckedChange` | `(checked: boolean \| 'indeterminate') => void` | Radix callback (boolean only in practice) |
| `id` / `aria-label` / `aria-describedby` | — | Label association |

**Not props:** hover, focus-visible, pressed (CSS `:focus-visible` / `:active`).

**Indeterminate:** Not in Figma Status axis — **not supported** in this component.

## Figma → code mapping

| Figma | Code |
|---|---|
| Status=Inactive | unchecked → `border-input`, `bg-[var(--custom-background-dark-input-30)]` |
| Status=Active | `data-[state=checked]` → `bg-primary border-primary` + Check icon |
| State=Focus | `:focus-visible` → `border-ring` + 3px `--custom-outline` |
| State=Disabled | `disabled` → `opacity-50` |
| State=Pressed | `:active` → `opacity-60` |
| Size 16×16 / radius 4 | `size-4` / `rounded-[4px]` |
| Label / Description | Composed in stories via `<label htmlFor>` |

## Token usage

`--primary`, `--primary-foreground`, `--input`, `--ring`, `--custom-background-dark-input-30`, `--custom-outline`, `--shadow-xs`

## Storybook coverage

Unchecked, Checked, DisabledUnchecked, DisabledChecked, FocusVisible, WithLabel, LongLabel, DarkMode

## Accessibility results

| Check | Result |
|---|---|
| Space toggles | Radix Checkbox |
| Checked state | `data-state` / ARIA from Radix |
| Label | `htmlFor` + clickable label in stories |
| Focus visible | 3px `--custom-outline` |
| Disabled | native disabled semantics |

## Visual parity results

Checked/unchecked fills, focus ring, disabled opacity, and 16px control match Figma. Light/Dark via Mode tokens.

## Known differences

1. **No indeterminate** — absent in Figma; not implemented.
2. **Label/description chrome** — Figma composite; code is control-only + story composition.
3. **Radius 4px** — Figma uses 4px; no exact Mode radius token (`radius-sm` is 6px) — uses literal `rounded-[4px]`.
4. **Geist** — deferred.
