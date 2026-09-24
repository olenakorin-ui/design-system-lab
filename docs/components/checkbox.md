# Checkbox — Figma ↔ code parity (v0.2)

Figma: [Checkbox `46:112`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=46-112)  
Code: `src/components/ui/checkbox.tsx`  
Stories: `src/components/ui/checkbox.stories.tsx`

## API

Uses Radix `Checkbox` Root props. Mixed selection is **`checked="indeterminate"`** (no separate React prop).

| Prop | Type | Notes |
|---|---|---|
| `checked` | `boolean \| 'indeterminate'` | Controlled; Unchecked / Checked / Indeterminate |
| `defaultChecked` | `boolean` | Uncontrolled initial (boolean only) |
| `disabled` | `boolean` | Figma State=Disabled |
| `onCheckedChange` | `(checked: boolean \| 'indeterminate') => void` | Radix callback |
| `id` / `aria-label` / `aria-describedby` | — | Label association |

**Not props:** hover, focus-visible, pressed (CSS).

## Figma → code mapping

| Figma / product | Code |
|---|---|
| Status=Inactive | unchecked → `border-input`, custom input fill |
| Status=Active | `data-[state=checked]` → primary fill + Check icon |
| **Indeterminate** (not in Figma Status axis) | `checked="indeterminate"` → primary fill + Minus icon; `aria-checked="mixed"` via Radix |
| State=Focus | `:focus-visible` → ring + `--custom-outline` |
| State=Disabled | `disabled` → opacity-50 |
| State=Pressed | `:active` → opacity-60 |

## Storybook

Unchecked, Checked, Indeterminate, DisabledIndeterminate, DisabledUnchecked, DisabledChecked, FocusVisible, WithLabel, LongLabel, DarkMode

## Accessibility

| Check | Result |
|---|---|
| Space toggles | Radix |
| `aria-checked="mixed"` | Radix when indeterminate |
| Focus visible | 3px `--custom-outline` |
| Disabled | native disabled |

## Known differences

1. **Indeterminate is a code extension** — Figma Status axis is still Active/Inactive only; recommend adding Status=Indeterminate in Figma for full visual ownership.
2. Label/description remain composed in stories (control-only API).
3. Radius 4px literal (no exact Mode radius token).
