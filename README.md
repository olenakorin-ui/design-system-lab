# Design System Lab

AI-ready design system experiment built on shadcn/ui.

## Goals
- Keep durable design-system rules in the repository.
- Mirror Figma Design System V2 into versioned tokens (then keep GitHub durable after parity).
- Document coded component behavior in Storybook.
- Make the system understandable to Codex/Cursor before generating prototypes.

## Current tokens (v0.4)

Architecture: **TailwindCSS → Theme → Mode** (Decision4=A).  
Source reference: [Design System V2](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2).

```text
tokens/primitive/   # 1. TailwindCSS
tokens/theme/       # 2. Theme
tokens/semantic/    # 3. Mode (Light/Dark)
tokens/custom/      # 4. Custom + Mode recipes
tokens/mappings/    # Figma → code/CSS (Decision3=B)
```

CSS (generated): `src/styles/tokens.css`  
Regenerate: `python3 scripts/migrate-tokens.py`  
Parity notes: `docs/figma-parity.md`  
Agent rules: `AGENTS.md`

## Coded components (v0.1)

Pipeline: Figma → tokens → semantic CSS → shadcn → React → Storybook.

| Component | Status | Docs |
|---|---|---|
| Button | Implemented | [`docs/components/button.md`](docs/components/button.md) |
| Input, Checkbox, Select, Badge, Alert, Dialog, Tabs | Planned | — |

```bash
npm install
npm run dev          # Vite app
npm run storybook    # Storybook (Light/Dark toolbar)
npm run build        # Typecheck + production build
```

## v0.1 scope
Token foundations are stable (v0.4.1 live Figma parity). Component work starts with **Button only**.
