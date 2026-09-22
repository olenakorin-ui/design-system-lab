# Figma ↔ GitHub parity

Last migration: **v0.4.1** (live Figma parity verified).  
Figma file: [Design System V2](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2) (`ZllxQplWi5QJcNeUHeY8T3`).  
Live extraction: `2026-09-22T10:50:30.250Z` → `tokens/_raw/figma-export.live.json` (760 variables).  
Assembler: `scripts/assemble-live-export.py` → curated `tokens/_raw/figma-export.json`.  
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
| ringOffset | A | Semantic `ring-offset` aliases Theme `background-*` (no synthetic Theme knobs) |
| customKeys | A | Preserve shorter v0.4 Mode `custom/*` keys; Figma names in mappings |

## Live parity status

**VALIDATED** against live MCP read-only export (`extractedAt` above).

| Check | Result |
|---|---|
| Collections | 4/4 — TailwindCSS 440, Theme 235, Mode 59, Custom 26 |
| Variables | 760 |
| Modes | Default / Default / Light+Dark / Desktop+Mobile |
| Text styles | 309 (count only; deferred) |
| Effect styles | 34 (count only; deferred) |
| codeSyntax | empty on all variables |
| Unresolved aliases | 0 |
| Name collisions | 0 |
| Missing mappings | 0 |

## Collection mapping

| Figma collection | Modes | Repo tier |
|---|---|---|
| `1. TailwindCSS` | Default | `tokens/primitive/` |
| `2. Theme` | Default | `tokens/theme/` |
| `3. Mode` | Light / Dark | `tokens/semantic/` (+ `custom/mode-recipes`) |
| `4. Custom` | Desktop / Mobile | `tokens/custom/layout` |

## Included in this migration

- All 760 live Figma variables inventoried in `_raw/figma-export.live.json`
- Curated production subset assembled for CSS (colors, spacing, radius, typography, shadow/blur, breakpoints, containers, Mode semantics, Mode custom recipes, Custom layout)
- Mode `base/ring-offset` → Theme `colors/background-light|dark` (Decision ringOffset=A)
- Mode `custom/*` short keys matching v0.4; exact Figma names in `mappings[].figma`

## Explicitly out of scope / deferred

| Item | Reason |
|---|---|
| Tailwind `width` / `height` / `min-width` / `line-height` utility floats in CSS layer | Inventoried live; not required for semantic CSS yet |
| Theme `inset-shadow` / `drop-shadow` vars | Present in live Theme; deferred beyond box-shadow + blur CSS |
| 309 Figma text styles | Style catalog; generate selectively later |
| 34 effect styles | Style objects; optional follow-up |
| Lab `success` / `warning` / `info` / `border-strong` / `surface-*` / `focus-ring` / `brand` | Decision2=B — not in Figma Mode |
| Motion durations | Spec-only; not in Figma variables |

## Parity checks (automated)

Run:

```bash
python3 scripts/assemble-live-export.py
python3 scripts/migrate-tokens.py
```

Inspect `tokens/_validation-report.json` for `parityStatus`, unresolved aliases, lab-only leaks, and duplicate CSS names.

## Known notes

- `primitive.color.neutral.0` is a convenience alias of white (documented in mappings; not a Figma variable).
- Mode `custom/*` Figma names containing spaces/`\` are sanitized to short keys; originals are preserved under `mappings[].figma`.
- Theme tier is first-class in JSON; CSS exposes `--theme-*-light|dark` knobs and Mode-facing `--primary` etc. via `var(--theme-…)`.
- Canonical live snapshot: `tokens/_raw/figma-export.live.json`. Curated migrator input: `tokens/_raw/figma-export.json`.

## Next parity upgrades

1. Optionally emit remaining Tailwind dimension utilities into CSS if components need them.
2. Catalog effect styles + text styles separately from variables.
3. Add Figma codeSyntax on variables if/when designers set it.
