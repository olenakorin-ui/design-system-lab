# Design System Token Specification v0.4

## Principles

- Three-tier architecture mirrors Figma: **TailwindCSS → Theme → Mode**.
- During migration, Figma Design System V2 is the design reference.
- After parity validation, GitHub (`tokens/**`) is the durable versioned source.
- Components consume **semantic** tokens (Mode), not raw primitives.
- Names are **normalized for code**; explicit Figma → code mappings live in `tokens/mappings/figma-to-code.json`.
- CSS is **generated only** from token JSON (`scripts/migrate-tokens.py` → `src/styles/tokens.css`).
- Do not invent lab-only tokens. Do not silently change semantics — log in `docs/decisions.md`.

## Architecture

```text
1. TailwindCSS (primitive)
   colors, spacing, opacity, border-width, rounded-*
        ↑ alias
2. Theme
   colors/*-light|dark, radius, font, text, shadow, blur, breakpoint, container
        ↑ alias
3. Mode (Light / Dark)
   base/* → semantic.color.{light|dark}.*
   alpha/*, custom/* recipes
4. Custom (Desktop / Mobile)
   heading-*, section/layout spacing
```

## Repository layout

```text
tokens/
  meta.json
  primitive/
    color.tokens.json
    dimension.tokens.json
  theme/
    color.tokens.json
    radius.tokens.json
    typography.tokens.json
    shadow.tokens.json
    layout.tokens.json
  semantic/
    color.tokens.json      # Mode base/* (light/dark)
    alpha.tokens.json
  custom/
    mode-recipes.tokens.json
    layout.tokens.json
  mappings/
    figma-to-code.json
  _raw/
    figma-export.json      # input snapshot for generator
src/styles/tokens.css        # GENERATED — do not hand-edit
scripts/migrate-tokens.py
```

## Naming (Decision 3 = B)

| Figma | Code path | CSS |
|---|---|---|
| `tailwind colors/blue/600` | `primitive.color.blue.600` | `--color-blue-600` |
| `colors/primary-light` | `theme.color.primary-light` | `--theme-primary-light` |
| `base/primary` (Mode) | `semantic.color.light.primary` | `--primary` |
| `spacing/4` | `primitive.dimension.spacing.4` | `--spacing-4` |
| `radius/md` | `theme.radius.md` | `--radius-md` |
| `alpha/90` | `semantic.alpha.light.90` | `--alpha-90` |

## Semantic colors (Mode `base/*`)

Production set (Light/Dark):  
`background`, `foreground`, `card`, `card-foreground`, `popover`, `popover-foreground`, `primary`, `primary-foreground`, `secondary`, `secondary-foreground`, `muted`, `muted-foreground`, `accent`, `accent-foreground`, `destructive`, `destructive-foreground`, `border`, `input`, `ring`, `ring-offset`, `sidebar*`, `chart-1`…`chart-5`.

**Removed from active production set (Decision 2 = B):** lab-only `success*`, `warning*`, `info*`, `error-subtle*`, `border-strong`, `surface-raised`, `surface-sunken`, `focus-ring`, and invented `brand/*`. Reintroduce only when they exist in Figma.

## Color direction (Decision 1 = A)

Figma blue/neutral theme wins.

- Light `primary` → Theme `primary-light` → `blue/600` (`#2563EB`)
- Dark `primary` → Theme `primary-dark` → `neutral/200`
- Neutrals are Tailwind Neutral (`#FAFAFA` … `#0A0A0A`), not the deprecated cool-neutral + indigo/violet lab palette.

## Deprecated

- v0.2 cool-neutral + indigo/violet direction (D001) — superseded by D003/D004.
- Flat `tokens/*.tokens.json` files at repo root of `tokens/` — removed in v0.4.
- `scripts/sync-figma-tokens.py` hardcoded snapshot — replaced by `scripts/migrate-tokens.py`.

## Regeneration

```bash
python3 scripts/migrate-tokens.py
```

Requires `tokens/_raw/figma-export.json`. Writes token tiers, mappings, CSS, and `tokens/_validation-report.json`.

## Motion

Motion tokens remain documented intent only (not present as Figma variables in V2):

- duration/fast = 100ms
- duration/normal = 150ms
- duration/moderate = 200ms
- duration/slow = 300ms
- easing/standard = cubic-bezier(0.2, 0, 0, 1)

## Component rule

No component is added until the semantic tokens it needs exist in Figma Mode (or an approved decision adds them), light/dark behavior is defined, and Figma/code APIs can align.
