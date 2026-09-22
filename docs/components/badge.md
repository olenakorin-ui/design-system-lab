# Badge — Figma ↔ code parity

Figma: [Badge `26:169`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=26-169)  
Code: `src/components/ui/badge.tsx`  
Stories: `src/components/ui/badge.stories.tsx`

## API (application state)

| Prop | Type | Notes |
|---|---|---|
| `variant` | `default` \| `secondary` \| `outline` \| `destructive` \| `verified` | Figma Variant axis only |
| `children` | `ReactNode` | Label and/or icons |
| `asChild` | `boolean` | Slot into another element |
| `className` | `string` | Escape hatch |

**Not props:** hover, focus (CSS only when applicable).

**Non-interactive by default** (`<span>`). Figma includes Hover/Focus visuals for catalog / interactive hosts; do not put `tabIndex` on Badge.

**No** `success` / `warning` / `info` variants (absent in Figma).

## Figma → code mapping

| Figma | Code |
|---|---|
| Variant=Default | `bg-primary text-primary-foreground` |
| Variant=Secondary | `bg-secondary text-secondary-foreground` |
| Variant=Outline | `bg-background border-border text-foreground` |
| Variant=Destructive | `bg-[var(--custom-destructive-dark-60)] text-white` |
| Variant=Verified | `bg-[var(--custom-blue-500-dark-blue-600)] text-white` |
| State=Hover | CSS `:hover` overlays / recipe fills |
| State=Focus | Not applied on non-interactive span; compose via `asChild` if host is focusable |
| Left/Right icons | Compose as `children`; decorative icons `aria-hidden` |
| text-xs / semibold / px-2 py-0.5 / gap-1 / rounded-md | Matching utilities |

## Token usage

`--primary`, `--primary-foreground`, `--secondary`, `--secondary-foreground`, `--background`, `--border`, `--foreground`, `--custom-destructive-dark-60|90`, `--custom-blue-500-dark-blue-600`, `--alpha-80`

No invented status tokens.

## Storybook coverage

Variants, WithLeftIcon, WithRightIcon, LongLabel, DarkMode

## Accessibility results

| Check | Result |
|---|---|
| Non-interactive | Default `<span>` — not in tab order |
| Decorative icons | `aria-hidden="true"` in stories |
| Name | Visible text children |

## Visual parity results

Variant fills match Mode semantics + custom recipes. Light/Dark Verified/Destructive recipes switch via `.dark`.

## Known differences

1. **Focus ring chrome** — Figma Focus frames use a nested Ring construct; non-interactive Badge omits focus styles unless composed with `asChild` onto a focusable host.
2. **Geist** — deferred.
3. **Hover Default** — approximated with `alpha/80` mix (same pattern as Button secondary hover).
