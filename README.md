# Design System Lab

AI-ready design system experiment built on shadcn/ui.

## Goals
- Keep durable design-system rules in the repository.
- Mirror semantic tokens into Figma Variables.
- Document coded component behavior in Storybook.
- Make the system understandable to Codex/Cursor before generating prototypes.

## Current tokens
v0.3 tokens are extracted from [Design System V2](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=580-9181) Figma variables (TailwindCSS + Theme + Mode + Custom).

Canonical files:
- `tokens/color.tokens.json`
- `tokens/spacing.tokens.json`
- `tokens/radius.tokens.json`
- `tokens/typography.tokens.json`
- `tokens/shadow.tokens.json`

CSS mirror: `src/styles/tokens.css`

## v0.1 scope
Foundations first: color, typography, spacing, radius, shadow, motion, light/dark modes.
Components follow only after token foundations are stable.
