# Interactive components v0.1 — parity review

Branch: `ds/interactive-components-v0.1`  
Order: Select → Alert → Tabs → Dialog

## Architectural findings

1. **Radix overlays scale** — Select/Dialog portals + focus management work with Mode tokens without inventing overlay semantics (Dialog overlay uses `black/80` until Figma adds a token).
2. **Alert stays strictly Figma-bound** — Default + Destructive only; no success/warning/info.
3. **Tabs Active fill** maps to existing `custom/background-dark-input-30`; list track uses `muted` (shadcn convention).
4. **Control vs composite** continues — Select/Dialog labels/actions composed with Button/stories.

## DECISION REQUIRED

None.
