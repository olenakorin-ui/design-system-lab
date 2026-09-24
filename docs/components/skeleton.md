# Skeleton — Figma ↔ code parity (v0.2)

Figma: [Skeleton `295:462`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=295-462)  
Code: `src/components/ui/skeleton.tsx`  
Stories: `src/components/ui/skeleton.stories.tsx`

## Scope

Minimal decorative loading placeholder. **No** product-specific skeleton compounds in the DS.

## API

| Prop | Notes |
|---|---|
| `className` | Size / radius / shape via utility classes |
| …div props | Standard |

Single export: `Skeleton`.

## Figma → code

| Figma | Code |
|---|---|
| `base/accent` fill | `bg-accent` |
| `rounded-md` / `rounded-full` | Via consumer `className` |
| Variant=Default / Card / Text compositions | **Stories** compose primitives (not DS variants) |
| Pulse | `animate-pulse` |

## Stories

Line, Block, MultipleLines, TableRows, DarkMode

## Accessibility

`aria-hidden="true"` on each `Skeleton`. Loading regions should set `aria-busy` / accessible name on a **wrapper**, not on each bar.

## Known differences

1. Figma ships Avatar+text / Card / Text composites as variants; code keeps a single primitive and documents composition in Storybook.
2. No shimmer token — pulse uses existing accent surface.
