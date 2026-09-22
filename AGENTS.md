# Design System Lab — Agent Guide

AI implementation partner for the Product Design workflow in this repository.

## Project

- Repository: https://github.com/olenakorin-ui/design-system-lab
- Figma: https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2
- Stack: Figma MCP, GitHub, React, TypeScript, Tailwind CSS, shadcn/ui, Storybook, Cursor (later Vercel)

## Role split

**ChatGPT owns:** product strategy, discovery, research planning, IA, flows, screen requirements, interaction models, experiments, sprint planning, business decisions, requirements, acceptance criteria, UX copy, analytics definitions.

**This agent owns:** repository implementation, Figma token extraction/normalization/codegen, Figma↔code parity, shadcn customization, React components, Storybook, coded prototypes, accessibility implementation, automated tests, git branches/commits, implementation docs, debugging, deployment prep.

## Decision boundary

Do not make product, UX, or business decisions silently. Do not invent product functionality to make implementation easier.

If implementation exposes an undefined UX/product choice, stop and report:

```text
DECISION REQUIRED
- Question
- Why it matters
- Option A
- Option B
- Technical implications
```

The user will resolve with ChatGPT and return a decision.

## Source model

```text
Figma
  ↕
Design tokens
  ↕
GitHub repository
  ↓
shadcn components
  ↓
Storybook
  ↓
Product prototypes
```

Figma Design System V2 is the starting design reference.

### Migration / parity

1. Inspect Figma first (variables, collections, modes, aliases, scopes, styles, component conventions).
2. Compare with the repository.
3. Produce a gap report before changing token architecture.
4. Preserve existing Figma naming unless documented otherwise.
5. Do not replace real Figma tokens with placeholder lab tokens.
6. After parity validation, GitHub is the durable versioned source layer.

When Figma and code disagree, report the discrepancy before choosing which version wins.

## Token rules

1. Prefer semantic tokens over raw values.
2. Components must not hardcode product colors.
3. Do not replace semantic tokens with raw primitives in product UI.
4. Preserve primitive → semantic → component relationships.
5. Preserve Figma aliases where possible.
6. Support Light/Dark modes if they exist in Figma.
7. Keep token naming deterministic.
8. Generate CSS from token definitions; do not maintain duplicated values manually.
9. Never silently change token semantics; record decisions in `docs/decisions.md`.
10. Treat `tokens/*.tokens.json` as the canonical token source; keep CSS mappings in sync.
11. Use `border` for low-emphasis separation; use `input` / `border-strong` for stronger control boundaries.
12. Prefer semantic status tokens (`success`, `warning`, `destructive`, `info`) over status primitives in product UI.

## Figma MCP

Before creating or modifying anything in Figma:

- inspect the existing file;
- inspect variables and collections;
- inspect component conventions;
- reuse existing system structures.

Do not recreate tokens or components that already exist.

## shadcn/ui

Use shadcn/ui as a code foundation, not the visual source of truth. Customize through our tokens and component APIs.

Do not:

- copy arbitrary shadcn colors into the system;
- hardcode Tailwind colors (e.g. `bg-blue-500`) when a semantic token exists;
- create duplicate components when an existing one can be extended;
- modify generated component APIs without documenting meaningful changes.

## Component parity

Aim for conceptual parity between Figma and code (variant, size, state, icon, loading, disabled). APIs need not be identical, but they should represent the same design-system concepts.

Rules for UI work:

1. Reuse an existing design-system component before creating a new one.
2. Keep Figma-facing names and code-facing APIs conceptually aligned.
3. Treat loading, empty, disabled, error, hover, focus, and selected as first-class states where relevant.
4. Do not create a new variant until checking whether an existing prop/state can represent the need.
5. Update Storybook when component behavior or states change.

## Storybook

Storybook is the coded behavior/documentation layer. Production-ready components should include stories for:

- default, variants, sizes
- hover, focus, disabled, loading
- error where relevant
- long content
- accessibility edge cases

Verify implementation in Storybook; screenshots alone are not sufficient evidence.

## Accessibility

Preserve:

- keyboard navigation
- visible focus
- semantic HTML
- accessible names
- contrast
- disabled semantics
- touch/click target requirements
- screen reader compatibility where relevant

Do not remove accessibility behavior inherited from Radix/shadcn.

## Git workflow

Before implementation:

1. inspect repository status;
2. read `README.md`, this file, `docs/token-spec.md`, `docs/decisions.md`.

Branch naming:

- `ds/<task>`
- `prototype/<feature>`
- `fix/<issue>`
- `experiment/<experiment>`

Use small, understandable commits. Do not mix unrelated refactors into feature commits.

## Documentation

Update docs when changing token architecture, component APIs, naming, source-of-truth rules, or Figma/code mappings.

Architectural decisions belong in `docs/decisions.md`. Do not rely only on chat history.

## Implementing UX specs from ChatGPT

Treat the provided UX specification as the product source for that implementation.

Before coding, summarize:

```text
IMPLEMENTATION PLAN
- screens
- components
- states
- interactions
- data assumptions
- technical assumptions
- unresolved UX questions
```

For each screen, include where specified: default, loading, empty, error, permission states, responsive behavior, accessibility, analytics hooks.

Do not omit non-happy-path states because the first screenshot only shows the happy path.

## Principle

The goal is not to show that AI can generate lots of code. The goal is a coherent product UI that correctly uses the design system, documented components, semantic tokens, accessibility rules, and UX specifications.

Prefer reuse and correctness over code volume.
