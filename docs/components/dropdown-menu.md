# Dropdown Menu — Figma ↔ code parity (v0.2)

Figma: [Dropdown Menu `89:189`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=89-189)  
Code: `src/components/ui/dropdown-menu.tsx`  
Stories: `src/components/ui/dropdown-menu.stories.tsx`

## API

Radix Dropdown Menu composition. No product-specific action names in the API.

| Export | Role |
|---|---|
| `DropdownMenu` | Root |
| `DropdownMenuTrigger` | Opens menu (`asChild` with Button common) |
| `DropdownMenuContent` | Panel (popover surface) |
| `DropdownMenuItem` | Action row; `variant="destructive"` for destructive styling |
| `DropdownMenuSeparator` | Divider |
| `DropdownMenuLabel` | Section label (Figma Label) |
| `DropdownMenuGroup` | Grouping |
| `DropdownMenuShortcut` | Right-aligned shortcut hint |
| `DropdownMenuCheckboxItem` / `RadioItem` | Figma Checkbox/Radio item variants |
| `DropdownMenuSub*` | Submenu (Figma SubTrigger) |

## Figma → code

| Figma | Code |
|---|---|
| DropdownMenu / Menu | `DropdownMenuContent` — `bg-popover border-border rounded-md p-1 shadow-md` |
| Item / Default | `DropdownMenuItem` — `px-2 py-1.5 rounded-sm`, focus → accent |
| Item / Label | `DropdownMenuLabel` — `font-semibold` |
| Item / Separator | `DropdownMenuSeparator` — `bg-border` |
| Item Error / destructive | `variant="destructive"` (uses Mode `destructive`, not invented status tokens) |
| Disabled | `data-[disabled]:opacity-50` |
| Shortcut | `DropdownMenuShortcut` muted |

## Stories

Default, Open, DisabledItem, DestructiveItem, LongLabels, DarkMode

## Accessibility

Radix: arrow-key navigation, typeahead, Escape closes, focus restore to trigger, disabled items skipped.

## Known differences

1. Avatar trigger / User item patterns deferred (Avatar not in Sprint 1).
2. Submenu included as primitives; not emphasized in primary stories.
3. Enter/exit motion uses generic animate classes if present; visual parity prioritized on open state chrome.
