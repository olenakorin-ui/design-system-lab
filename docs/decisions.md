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
