# Select — Figma ↔ code parity

Figma: [Select `345:11530`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=345-11530), Menu Item `118:1541`, Menu `118:2501`  
Code: `src/components/ui/select.tsx`

## API

| Export | Role |
|---|---|
| `Select` | Root (`value` / `defaultValue` / `onValueChange` / `disabled` / `open`) |
| `SelectTrigger` | Trigger button |
| `SelectValue` | Placeholder / selected text |
| `SelectContent` | Popover list |
| `SelectItem` | Option |
| `SelectGroup` / `SelectLabel` / `SelectSeparator` | Grouping |

Open/hover/focus owned by Radix + CSS.

## Figma → code

| Figma | Code |
|---|---|
| Trigger Default | `h-9`, `border-input`, `bg-[var(--custom-background-dark-input-30)]`, `shadow-xs` |
| Placeholder | `data-[placeholder]:text-muted-foreground` |
| Filled value | `text-foreground` |
| Focus / open | `border-ring` + 3px `--custom-outline` |
| Disabled | `disabled:opacity-50` |
| Menu | `bg-popover border-border rounded-md` |
| Item Hover/Focus | `focus:bg-accent focus:text-accent-foreground` |
| Selected | Check indicator (Figma Checkbox item variant metaphor) |

## Tokens

`--input`, `--ring`, `--custom-background-dark-input-30`, `--custom-outline`, `--popover`, `--border`, `--accent`, `--muted-foreground`, `--foreground`

## Stories

Default, WithValue, Placeholder, Disabled, OpenState, LongOptions, ManyOptions, DarkMode

## Accessibility

Radix Select: arrows, Enter/Space, Escape, typeahead, focus restore, selected announcement.

## Known differences

1. Label/description composite — stories only.
2. Item Checkbox/Icon types — not separate variants; checkmark for selected.
3. Open Focus empty trigger Figma tint (`custom/accent-dark-input-50`) — approximated by shared focus/open ring (not accent fill).
4. Geist deferred.
