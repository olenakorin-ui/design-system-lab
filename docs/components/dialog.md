# Dialog — Figma ↔ code parity

Figma: [Dialog `112:602`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=112-602)  
Code: `src/components/ui/dialog.tsx`

## API

| Export | Role |
|---|---|
| `Dialog` | Root open state |
| `DialogTrigger` / `DialogClose` | Open / dismiss |
| `DialogContent` | Panel + optional close (`showCloseButton`) |
| `DialogHeader` / `DialogFooter` | Layout regions |
| `DialogTitle` / `DialogDescription` | Accessible title/description |
| `DialogOverlay` | Scrim |

## Figma → code

| Figma | Code |
|---|---|
| Panel | `bg-background border-border rounded-lg` |
| Title | `text-foreground font-semibold` |
| Description | `text-muted-foreground text-sm` |
| Close | Icon button + `sr-only` “Close” |
| Footer actions | Compose `Button` |
| Breakpoint lg/sm | Responsive classes (`sm:`) |
| Overlay | Not in Figma set → `bg-black/80` |

## Stories

Default, LongContent, DestructiveConfirm, NoCloseIcon, DarkMode

## Accessibility

Radix: focus trap, Escape, labelled by title, described by description, focus restore, overlay blocks background.

## Known differences

1. Overlay color not tokenized in Figma Dialog — uses `black/80`.
2. Destructive confirm is composition (Button destructive), not a Dialog variant.
3. Geist deferred.
