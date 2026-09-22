# Button — Figma ↔ code parity

Figma: [Button `37:931`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=37-931)  
Code: `src/components/ui/button.tsx`  
Stories: `src/components/ui/button.stories.tsx`

## API (application state)

| Prop | Type | Notes |
|---|---|---|
| `variant` | `default` \| `secondary` \| `destructive` \| `outline` \| `ghost` \| `link` | Maps Figma Variant (Default → `default`) |
| `size` | `default` \| `sm` \| `lg` \| `icon` | Maps Figma Size |
| `disabled` | `boolean` | Figma State=Disabled (layer opacity 0.5) |
| `loading` | `boolean` | Figma State=Loading (layer opacity 0.5 + LoaderCircle) |
| `asChild` | `boolean` | Radix Slot. **Unsupported with `loading`** (falls back to `<button>`) |
| `children` | `ReactNode` | Label and/or icons |
| native button attrs | — | `type`, `aria-label`, `onClick`, … |

**Not props (CSS only):** hover, focus-visible, active/pressed.

### `asChild` + `loading`

**Not recommended / unsupported.** Loading injects a spinner sibling and expects a real `<button>`. Combining with `asChild` (Slot) is unreliable; when both are set, code ignores `asChild` and renders `<button>`.

## Figma → code mapping

| Figma | Code |
|---|---|
| Variant=Default | `variant="default"` → `bg-primary` / `text-primary-foreground` |
| Variant=Secondary | `variant="secondary"` → `bg-secondary` / `text-secondary-foreground` |
| Variant=Destructive | `variant="destructive"` → `bg-[var(--custom-destructive-dark-60)]` |
| Variant=Outline | `variant="outline"` → border `input`, fill `--custom-background-dark-input-30` |
| Variant=Ghost | `variant="ghost"` → transparent / hover `accent` |
| Variant=Link | `variant="link"` → `text-primary`; Hover → `underline` (Figma `textDecoration: UNDERLINE`) |
| Size=default | `size="default"` → `h-9 px-4` |
| Size=sm | `size="sm"` → `h-8 px-3` |
| Size=lg | `size="lg"` → `h-10 px-8` |
| Size=icon | `size="icon"` → `size-9` |
| State=Hover | CSS `:hover` (token overlays / recipe fills) |
| State=Focus | CSS `:focus-visible` → 3px `--custom-outline` (Destructive → `--custom-destructive-20-dark-40`) |
| State=Pressed | CSS `:active` → `opacity-60` (Figma layer opacity `0.6`) |
| State=Disabled | `disabled` → `opacity-50` (Figma layer opacity `0.5`) |
| State=Loading | `loading` + Lucide `LoaderCircle` → `opacity-50` |
| Left/Right Icon | compose Lucide (or other) icons as `children` |
| shadow/xs | `shadow-xs` → `--shadow-xs` |
| radius rounded-md | `rounded-md` → `--radius-md` (8px) |
| text/sm + medium | `text-sm font-medium` |
| gap spacing/2 | `gap-2` (8px) |

## Token usage

Consumes Mode semantic CSS variables from `src/styles/tokens.css`:

- Surfaces/text: `--primary`, `--primary-foreground`, `--secondary`, `--secondary-foreground`, `--accent`, `--accent-foreground`, `--foreground`, `--destructive-foreground`, `--input`, `--ring`
- Recipes: `--custom-destructive-dark-60|90`, `--custom-destructive-20-dark-40`, `--custom-background-dark-input-30`, `--custom-accent-dark-input-50`, `--custom-outline`
- Overlay: `--alpha-90`, `--alpha-80`
- Layout: `--radius-md`, `--shadow-xs`, `--font-sans`

No hardcoded product hex in the component. No invented status tokens.

### Opacity dependency (no broad `--opacity-*` CSS emit yet)

Figma Button uses **layer opacity**:

| Figma state | Measured opacity | Code |
|---|---:|---|
| Disabled / Loading | `0.5` | Tailwind `opacity-50` |
| Pressed (`:active`) | `0.6` | Tailwind `opacity-60` |

These match Figma `opacity/opacity-50` and `opacity/opacity-60` numeric values (`50` / `60` percent in `tokens/primitive/dimension.tokens.json`). Primitive opacity CSS vars are **not** emitted into `tokens.css` yet; Button depends on Tailwind’s built-in `opacity-50` / `opacity-60` until a future token codegen decision. Do not invent component-local opacity tokens.

## Storybook coverage

- Default, Variants, Sizes, Disabled, Loading, WithIcon, IconOnly, LongLabel, FocusVisible
- Toolbar: Light / Dark (`.dark` on `html`)

## Accessibility results

| Check | Result |
|---|---|
| Keyboard | Native `<button>` — Tab focus, Enter/Space activate |
| Accessible name | Text children; IconOnly stories require `aria-label` |
| Focus visibility | `:focus-visible` 3px outline shadow (not mouse-only `:focus`) |
| Disabled | `disabled` + `pointer-events-none` + opacity 50; not focusable when disabled |
| Loading | `aria-busy="true"`; interaction disabled; spinner `aria-hidden`; icon-only exposes “Loading” via `sr-only` |
| Contrast | Light Default primary `#2563EB` on `#FAFAFA` foreground — passes; Dark primary `#E5E5E5` on `#171717` — passes. Destructive uses Mode recipes. Validate per theme in Storybook a11y addon. |

## Visual parity results

| Area | Status |
|---|---|
| Sizes / padding / radius / gap / type size | Match Figma |
| Variant fills (default/secondary/ghost/link) | Match semantic tokens |
| Outline / Destructive fills | Match custom Mode recipes |
| Focus ring geometry | Match 3px spread `custom/outline` |
| Loading / Disabled opacity | Match 50% via `opacity-50` |
| Pressed opacity | Match 60% via `opacity-60` |
| Hover Default | Match intent via `--alpha-90` overlay on primary |
| Hover Link | Match Figma underline on hover |
| Hover Secondary | **Parity gap** — approximated (no dedicated token) |
| Font family | Geist deferred; `--font-sans` falls back to `system-ui` |
| Spinner | Lucide `LoaderCircle` (Figma uses same metaphor) |

## Known differences

1. **Hover Secondary (parity gap)** — Figma stacks `base/secondary` + `alpha/80` with paint opacity `0.2`. Searched Mode variables: no dedicated secondary-hover / recipe token (only `base/secondary`, `alpha/80`, and unrelated `custom/accent dark:input\\50`). Code approximates with `color-mix(in srgb, var(--alpha-80) 20%, transparent)` overlay on `bg-secondary`. Revisit if Figma adds an explicit hover recipe.

2. **Geist font** — deferred; not bundled. Token lists Geist; CSS falls back to `system-ui`.

3. **Opacity primitives in CSS** — not emitted yet; Button uses Tailwind `opacity-50` / `opacity-60` which match Figma’s `0.5` / `0.6` layer opacities (see Opacity dependency above).

4. **`asChild` + `loading`** — unsupported; loading forces a real `<button>`.

## Pipeline proven

```text
Figma Button → Mode tokens → tokens.css → Tailwind @theme → shadcn Button → Storybook
```
