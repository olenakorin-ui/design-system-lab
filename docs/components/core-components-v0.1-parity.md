# Core components v0.1 — parity review

Branch: `ds/core-components-v0.1`  
Sprint: Input → Checkbox → Badge (sequential)  
Baseline: Button architecture on `main` (`f2b70ae`)

## Architectural findings

1. **Control vs composite** — Figma Input/Checkbox are field+label+description composites. Code ships **controls** with story-level composition (same pattern as Button). Scales cleanly; FormField wrapper can come later without inventing tokens.
2. **CSS interaction states stay in CSS** — Focus/Hover/Pressed never became React props.
3. **Semantic + Mode recipes only** — No `success` / `warning` / `info`. Badge `verified` uses existing `custom/blue-500-dark-blue-600`.
4. **Radix where interaction needs it** — Checkbox uses `@radix-ui/react-checkbox`; Input/Badge stay native/`span`.
5. **Indeterminate** — Inspected Checkbox; Figma has only Inactive/Active — not implemented.

## Component status

| Component | Commit intent | Docs |
|---|---|---|
| Input | `feat: add input component and stories` | `docs/components/input.md` |
| Checkbox | `feat: add checkbox component and stories` | `docs/components/checkbox.md` |
| Badge | `feat: add badge component and stories` | `docs/components/badge.md` |

## Shared validation

| Check | Result |
|---|---|
| Light/Dark | Storybook theme toolbar + DarkMode stories |
| `npm run build` | Pass (per component + final) |
| `npm run build-storybook` | Pass (per component + final) |
| DECISION REQUIRED | None |

## Deferred across the set

- Geist font bundling
- Emitting `--opacity-*` CSS vars (Tailwind `opacity-50/60` used)
- Input File composite chrome / horizontal layout FormField
- Checkbox label composite as a product component
- Badge focus ring when non-interactive
