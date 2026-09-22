# Tabs — Figma ↔ code parity

Figma: [Tabs / Trigger `183:532`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=183-532)  
Code: `src/components/ui/tabs.tsx`

## API

`Tabs`, `TabsList`, `TabsTrigger`, `TabsContent` — Radix controlled via `value` / `defaultValue` / `onValueChange`.

## Figma → code

| Figma | Code |
|---|---|
| Active=On | `data-[state=active]:bg-[var(--custom-background-dark-input-30)] shadow-sm` |
| Active=Off | transparent on muted list |
| Focus | `focus-visible:shadow-[0_0_0_3px_var(--custom-outline)]` |
| Disabled | `disabled:opacity-50` |

## Stories

Default, ManyTabs, LongLabels, DisabledTab, FocusVisible, DarkMode

## Accessibility

Radix tablist/tab/tabpanel, arrow keys, `aria-selected`, roving tabindex.

## Known differences

1. List chrome uses `bg-muted` track (common shadcn) — Figma page sample is bare triggers; Active fill matches Figma.
2. Icon/Badge trigger props deferred.
3. Geist deferred.
