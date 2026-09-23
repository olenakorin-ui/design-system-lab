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

---

## D004 — Three-tier migration + architecture decisions 1–4

### Context
Gap analysis compared Figma Design System V2 (760 variables, 4 collections) with the flattened v0.3 repo import. Four architecture decisions were approved before further migration.

### Options considered
See gap analysis Decision Required items (brand direction, lab-only semantics, naming fidelity, Theme tier).

### Decision
1. **A** — Figma blue/neutral theme wins (deprecate indigo/violet lab direction for production tokens).
2. **B** — Remove lab-only semantic tokens (`success*`, `warning*`, `info*`, `error-subtle*`, `border-strong`, `surface-*`, `focus-ring`, invented `brand/*`) from the active production set unless they exist in Figma.
3. **B** — Normalize names for code; maintain explicit Figma → repo/CSS mappings in `tokens/mappings/figma-to-code.json`.
4. **A** — Preserve three-tier architecture: TailwindCSS → Theme → Mode in `tokens/{primitive,theme,semantic,custom}/`.

### Reason
Keeps GitHub aligned with the implemented Figma system, avoids placeholder drift, and makes theming (Theme knobs) + mode switching (Mode) first-class in code.

### Impact
- Token files restructured; CSS generated only from JSON via `scripts/migrate-tokens.py`.
- D001 indigo/violet production use superseded for active tokens (historical record retained).
- Status/surface lab tokens require a future Figma + product decision before reuse.
- `docs/figma-parity.md` tracks included/deferred parity items.

### Revisit when
Live full-variable re-export is run; or product adds Figma Mode tokens for status/surfaces; or brand theming changes Theme `primary-*` aliases.

---

## D005 — Live Figma parity: ring-offset alias + custom key stability

### Context
Live MCP re-export (2026-09-22) showed Mode `base/ring-offset` aliases Theme `colors/background-*`, not invented `colors/ring-offset-*`. Mode `custom/*` sanitizer also risked longer keys that would churn CSS names.

### Options considered
- ring-offset: (A) alias Theme background; (B) keep synthetic Theme knobs; (C) ask design to add Theme ring-offset tokens
- custom keys: (A) keep shorter v0.4 keys; (B) accept live-derived longer keys

### Decision
- **ringOffset=A** — Semantic `ring-offset` aliases `theme.color.background-{light|dark}`; do not invent Theme `ring-offset-*`.
- **customKeys=A** — Preserve shorter v0.4 normalized keys; keep exact Figma names in mappings; sanitizer collapses repeated stems.

### Reason
Faithful to live Figma alias graph without inventing Theme tokens; stable CSS for consumers.

### Impact
- `modeBaseThemeTargets` in curated export / semantic meta
- CSS: `--ring-offset: var(--theme-background-light|dark)`
- Live inventory at `tokens/_raw/figma-export.live.json`; parity documented in `docs/figma-parity.md`

### Revisit when
Design adds Theme `colors/ring-offset-*` in Figma, or product needs distinct ring-offset knobs independent of background.

---

## D006 — Storybook vs Prototype Lab

### Context
Experiment 01 (Access Request Review) was first exercised heavily via Storybook. Product workflows need deployable sharing, routing, mocked scenarios, and end-to-end interaction that do not belong in component documentation.

### Options considered
- Keep prototypes primarily in Storybook (pages as stories)
- Dedicated Prototype Lab SPA + Storybook for DS only
- Separate repository for prototypes

### Decision
- **Storybook** = component documentation, states, Figma parity, accessibility validation, component regression.
- **Prototype Lab** (`src/prototype-shell` + `src/prototypes`) = pages, product flows, mocked data, product states, E2E interactions, external sharing, experiment validation.
- Prototype Storybook stories may remain as **internal regression only**, not the primary runtime or sharing path.

### Reason
Preserves Storybook as the DS contract surface while giving product experiments a normal web app lifecycle (routes, query scenarios, deployable `dist/`).

### Impact
- App entry mounts `PrototypeRouter` (hub + client History routes).
- Registry at `src/prototypes/registry.ts`.
- Architecture guide: `docs/prototype-architecture.md`.
- Branches: prefer `prototype/<flow-name>` for durable flows; `experiment/*` for DS usage experiments.

### Revisit when
Multiple apps need isolation, or deployment/auth requirements exceed a static SPA.

---

## D007 — Prototype Lab host: Vercel

### Context
Prototype Lab needs SPA fallback for client routes (`/`, `/prototypes/...`, scenario query deep links). Host choice determines rewrite config.

### Options considered
- A — Netlify (`public/_redirects`)
- B — Vercel (`vercel.json` rewrites)
- C — Defer deploy; local/preview only

### Decision
**B — Vercel.** Use `vercel.json` rewrites so non-asset paths fall back to `index.html`. Build output remains Vite `dist/`.

**Deployment method (2026-09-23):** Connect the GitHub repository in the Vercel dashboard via **Git integration** (not local CLI login).

| Git ref | Vercel deployment |
|---|---|
| `main` | Production — stable Prototype Lab |
| `prototype/*` | Preview — new flows |
| `concept/*` | Preview — alternative concepts |
| `experiment/*` | Optional preview |

### Reason
Matches the approved host choice for first external sharing of Prototype Lab. Git integration gives branch previews without requiring a local Vercel CLI session.

### Impact
- `vercel.json` checked in on `prototype/lab-shell`
- Netlify `_redirects` not used
- First preview requires a one-time Vercel ↔ GitHub project import (human dashboard step)
- External reviewers get Prototype Lab URLs, not Storybook

### Revisit when
Hosting moves off Vercel, or Storybook needs a separate deploy target.

---

## D008 — Preview sharing: protected + shareable bypass

### Context
Experiment 02 Preview URLs required Vercel SSO login, blocking unauthenticated/incognito external reviewers.

### Options considered
- A — Keep SSO only (collaborators with Vercel/GitHub access)
- B — Disable Deployment Protection on Preview (fully public)
- C — Keep protection; use a shareable external-access method

### Decision
**C.** Previews stay protected (SSO remains for default visitors). External reviewers receive a **shareable Protection Bypass** URL (or equivalent password/share link from the Vercel dashboard), not a fully public Preview.

### Reason
Balances Prototype Lab confidentiality with the need to share flows outside the Vercel org without making every Preview world-readable.

### Impact
- Project setting: **Protection Bypass** enabled for `design-system-lab` (automation/share secret).
- Share pattern: append `x-vercel-protection-bypass=<secret>` (and optionally `x-vercel-set-bypass-cookie=true`) to Prototype Lab Preview URLs — **never commit the secret**.
- Production on custom domains can remain separately reachable per existing SSO `all_except_custom_domains` setting.
- Documented in `docs/prototype-architecture.md` § External sharing.

### Revisit when
Team standardizes on Password Protection instead of Bypass, or Preview Protection is relaxed for `prototype/*` only.

