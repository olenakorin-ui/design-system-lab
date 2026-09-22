# Alert — Figma ↔ code parity

Figma: [Alert `26:160`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=26-160)  
Code: `src/components/ui/alert.tsx`

## API

| Export | Notes |
|---|---|
| `Alert` | `role="alert"`, `variant?: 'default' \| 'destructive'` |
| `AlertTitle` | Title text |
| `AlertDescription` | Supporting text |
| children | Optional decorative icon (first SVG) |

**No** success / warning / info. Optional Figma Button action not in v0.1 API.

## Figma → code

| Figma | Code |
|---|---|
| Default | `bg-card border-border text-foreground`; description `muted-foreground` |
| Destructive | `bg-destructive-foreground border-destructive text-destructive` |
| radius lg / padding | `rounded-lg px-4 py-3` |
| Icon | Compose Lucide child; `aria-hidden` when decorative |

## Stories

Default, Destructive, TitleOnly, DescriptionOnly, WithIcon, LongContent, DarkMode

## Accessibility

`role="alert"`; decorative icons hidden; non-interactive container.

## Known differences

1. Optional Undo button from Figma not shipped — compose with Button outside if needed.
2. Geist deferred.
