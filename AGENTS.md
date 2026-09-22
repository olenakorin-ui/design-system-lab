# Design System Lab — Agent Guide

Repository-wide, tool-independent rules for agents working in this project.

Cursor-specific working behavior lives in `.cursor/rules/` — do not duplicate procedural formats here.

## Project

- Repository: https://github.com/olenakorin-ui/design-system-lab
- Figma: https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2
- Stack: Figma MCP, GitHub, React, TypeScript, Tailwind CSS, shadcn/ui, Storybook, Cursor (later Vercel)

## Role split

**ChatGPT owns:** product strategy, discovery, research planning, IA, flows, screen requirements, interaction models, experiments, sprint planning, business decisions, requirements, acceptance criteria, UX copy, analytics definitions.

**Implementation agents own:** repository work, token extraction/normalization/codegen, Figma↔code parity, shadcn customization, React components, Storybook, prototypes, accessibility implementation, tests, git, implementation docs, debugging, deployment prep.

Unresolved UX/product/business choices are not decided by implementation agents. Use the `DECISION REQUIRED` workflow defined in `.cursor/rules/implementation-partner.mdc`.

## Source of truth

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

- Figma Design System V2 is the starting design reference during migration.
- Inspect Figma (variables, collections, modes, aliases, scopes, styles, conventions) before changing it or the token architecture.
- Produce a gap report before changing token architecture.
- Preserve Figma naming unless a documented decision says otherwise.
- Do not invent design-system tokens or replace real Figma tokens with placeholders.
- Do not invent component behavior that is not in the design system or UX spec.
- After migration parity is validated, **GitHub is the durable versioned source layer**.
- When Figma and code disagree, report the discrepancy before choosing a winner.

Canonical token files: `tokens/{primitive,theme,semantic,custom}/**/*.tokens.json` plus `tokens/mappings/`. Keep generated CSS (`src/styles/tokens.css`) synchronized via `scripts/migrate-tokens.py`.

## Token policy

1. Prefer semantic tokens over raw values.
2. Components must not hardcode product colors or use raw primitives in product UI.
3. Preserve primitive → semantic → component relationships and Figma aliases where possible.
4. Support Light/Dark modes when they exist in Figma.
5. Keep token naming deterministic.
6. Generate CSS from token definitions; do not hand-maintain duplicate values.
7. Never silently change token semantics; record decisions in `docs/decisions.md`.
8. Use Mode semantic tokens for surfaces and controls (`border`, `input`, `ring`) as defined in Figma — do not invent extra boundary tokens unless they exist in Figma or an approved decision adds them.
9. Do not invent status tokens (`success`, `warning`, `info`, …) in the production set until they exist in Figma Mode (see D004 / Decision2=B). Use `destructive` and other Mode `base/*` tokens that already exist.

## Component policy

1. Reuse an existing design-system component before creating a new one.
2. Keep Figma concepts and code APIs conceptually aligned (variant, size, state, icon, loading, disabled).
3. Treat loading, empty, disabled, error, hover, focus, and selected as first-class states where relevant.
4. Do not create a new variant until an existing prop/state cannot represent the need.
5. Non-happy-path states are required when specified in the UX spec — do not omit them because the first screenshot is happy-path only.
6. Update Storybook when component behavior or states change.

shadcn/ui is a code foundation, not the visual source of truth. Customize through our tokens and APIs. See `.cursor/rules/design-system.mdc` for Cursor implementation constraints.

## Accessibility

Preserve keyboard navigation, visible focus, semantic HTML, accessible names, contrast, disabled semantics, touch/click targets, and screen reader compatibility where relevant. Do not remove accessibility behavior inherited from Radix/shadcn.

## Git workflow

Before implementation: check git status; read `README.md`, this file, `docs/token-spec.md`, and `docs/decisions.md`.

Branches: `ds/<task>`, `prototype/<feature>`, `fix/<issue>`, `experiment/<experiment>`.

Use small, understandable commits. Do not mix unrelated refactors into feature commits.

## Documentation

Update docs when changing token architecture, component APIs, naming, source-of-truth rules, or Figma/code mappings. Architectural decisions belong in `docs/decisions.md`. Do not rely only on chat history.

## Principle

Prefer reuse and correctness over code volume. The goal is a coherent product UI that uses the design system, semantic tokens, accessibility rules, and UX specifications — not demonstrating that AI can generate lots of code.
