# Design System Decision Log

Use this format for meaningful decisions.

## Decision

### Context

### Options considered

### Decision

### Reason

### Impact

### Revisit when


---

## D001 — Color direction: cool-neutral + indigo/violet

### Context
The v0.1 system needed a neutral-first B2B palette with enough brand character for AI/product tooling without becoming visually noisy or cyberpunk.

### Options considered
- Generic blue + neutral
- Warm gray + purple
- Cool neutral + indigo/violet

### Decision
Use a cool-neutral scale as the structural UI palette and an indigo/violet scale as the brand/action palette.

### Reason
The neutral scale supports dense admin UI and readable light/dark surfaces. The indigo/violet brand creates a more distinctive identity than default SaaS blue while remaining practical for actions, focus, selected states, and branded accents.

### Impact
Semantic tokens map to the neutral and brand primitives rather than hardcoded values. Status colors remain independent from brand.

### Revisit when
Visual direction testing shows the brand hue is too expressive or too muted for the target portfolio/product context.

---

## D002 — Separate decorative borders from interactive control boundaries

### Context
A subtle decorative border can be visually appropriate but may not provide enough non-text contrast when the boundary is necessary to identify a control.

### Decision
Keep `border` subtle, while mapping `input` and `border-strong` to stronger neutrals. Focus rings use the brand scale.

### Reason
This lets cards/dividers remain quiet while interactive controls and focus states remain more identifiable.

### Impact
Component recipes must use `input` for interactive control boundaries rather than assuming `border` is appropriate everywhere.

### Revisit when
Component accessibility QA indicates stronger or weaker boundaries are needed.

---

## D003 — Import Design System V2 Figma tokens as v0.3 source

### Context
The lab v0.2 palette (cool-neutral + indigo/violet) was a placeholder direction. The working Figma file [Design System V2](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=580-9181) already contains a complete shadcn/ui variable set.

### Options considered
- Keep v0.2 lab values and only document Figma separately
- Extract Figma variables into the repository as the canonical token source

### Decision
Extract Figma collections `1. TailwindCSS`, `2. Theme`, `3. Mode`, and `4. Custom` into `/tokens/*.tokens.json` and mirror them in `/src/styles/tokens.css`.

### Reason
The Figma file is the implemented visual system. Aligning code tokens with Mode/Theme aliases prevents drift between design and code.

### Impact
- Neutral primitives switch from cool-neutral to Tailwind Neutral.
- Brand/primary in light mode aliases `blue/600` (`#2563EB`); dark primary aliases `neutral/200`.
- Spacing, radius, typography, shadows, chart, and sidebar tokens are now first-class.
- Lab-only status tokens (`success`, `warning`, `info`, `border-strong`, `surface-*`) remain as extensions on top of the Figma set.

### Revisit when
A custom brand palette replaces the default shadcn blue/neutral theme in Figma.
