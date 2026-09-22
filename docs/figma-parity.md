# Figma ↔ GitHub parity

Last migration: **v0.4.0** (three-tier token architecture).  
Figma file: [Design System V2](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2) (`ZllxQplWi5QJcNeUHeY8T3`).  
Generator: `scripts/migrate-tokens.py`  
Validation: `tokens/_validation-report.json`  
Mappings: `tokens/mappings/figma-to-code.json`

## Decisions applied

| ID | Choice | Effect |
|---|---|---|
| Decision1 | A | Figma blue/neutral theme wins |
| Decision2 | B | Lab-only semantics removed from production set |
| Decision3 | B | Normalized code names + explicit Figma mappings |
| Decision4 | A | Preserve TailwindCSS → Theme → Mode |

## Collection mapping

| Figma collection | Modes | Repo tier |
|---|---|---|
| `1. TailwindCSS` | Default | `tokens/primitive/` |
| `2. Theme` | Default | `tokens/theme/` |
| `3. Mode` | Light / Dark | `tokens/semantic/` (+ `custom/mode-recipes`) |
| `4. Custom` | Desktop / Mobile | `tokens/custom/layout` |

## Included in this migration

- All Tailwind color scales present in the export snapshot
- Spacing, opacity, border-width, rounded-* (with Theme radius aliases)
- Theme color knobs (`*-light` / `*-dark`) for every Mode `base/*` token
- Theme radius, typography (font/text/weights), shadow, blur, breakpoint, container
- Mode `base/*` semantics (light/dark)
- Mode `alpha/*`
- Mode `custom/*` recipes (normalized keys; original Figma names in mappings)
- Custom collection heading + section layout tokens

## Explicitly out of scope / deferred

| Item | Reason |
|---|---|
| Full re-pull of all 760 vars via live MCP in this pass | Repo-only constraint; snapshot assembled from prior discovery + v0.3 |
| Tailwind `width` / `height` / `min-width` / `line-height` utility floats | Not required for semantic CSS layer yet; can import in a follow-up |
| 309 Figma text styles | Style catalog, not variable tokens; generate selectively later |
| Effect styles beyond Theme shadow/blur vars (`inset-shadow`, `drop-shadow`, `backdrop-blur`, `focus/*`) | Style objects; optional follow-up |
| Lab `success` / `warning` / `info` / `border-strong` / `surface-*` / `focus-ring` / `brand` | Decision2=B — not in Figma Mode |
| Motion durations | Spec-only; not in Figma variables |

## Parity checks (automated)

Run `python3 scripts/migrate-tokens.py` and inspect `tokens/_validation-report.json`:

- unresolved aliases
- lab-only leaks into semantic set
- duplicate normalized CSS variable names
- token counts per tier

## Known notes

- `primitive.color.neutral.0` is a convenience alias of white (documented in mappings).
- Mode `custom/*` Figma names containing spaces/`\` are sanitized for code keys; original strings are preserved under `mappings[].figma`.
- Theme tier is first-class in JSON; CSS exposes both `--theme-*-light|dark` knobs and Mode-facing `--primary` etc. via `var(--theme-…)`.
- Source snapshot path: `tokens/_raw/figma-export.json` (refresh from Figma in a future sync pass when MCP re-export is approved).

## Next parity upgrades

1. Live Figma re-export of all 760 variables into `_raw` (read-only MCP).
2. Import remaining Tailwind dimension utilities if components need them.
3. Catalog effect styles + text styles separately from variables.
4. Add Figma codeSyntax on variables if/when designers set it.
