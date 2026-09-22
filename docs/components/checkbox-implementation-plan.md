# IMPLEMENTATION PLAN — Checkbox v0.1

Figma source: [Checkbox `46:112`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=46-112)

## Scope

Implement the **checkbox control** via `@radix-ui/react-checkbox` (shadcn pattern). Label/description composition is consumer-side (stories).

## Figma inventory

- **Status:** Inactive | Active — **no Indeterminate**
- **State:** Default, Focus, Disabled, Pressed (CSS for Focus/Pressed; React for Disabled + checked)
- Control: 16×16, radius 4px, check icon when Active
- Tokens: Inactive fill `custom/background dark:input\\30` + `base/input` stroke; Active `base/primary`; focus `custom/outline`; disabled opacity 50; pressed opacity 60

## API

`checked` | `defaultChecked` | `disabled` | `onCheckedChange` (+ className)

Do **not** expose indeterminate (absent in Figma).

## Stories

Unchecked, Checked, DisabledUnchecked, DisabledChecked, FocusVisible, WithLabel, LongLabel, DarkMode
