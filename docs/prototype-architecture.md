# Prototype architecture

## 1. Purpose

Separate **Design System component validation** from **product workflow validation**.

- **Storybook** = Design System component validation only (docs, states, Figma parity, a11y, regression). **Not** the external product-prototype environment.
- **Prototype Lab** = product-flow runtime (pages, mocks, scenarios, external sharing).

## 2. Storybook vs Prototype Lab

| | Storybook | Prototype Lab |
|---|---|---|
| Audience | Design system authors / implementers | Product / UX / stakeholders |
| Content | Components, states, Figma parity, a11y | Pages, flows, mocked data, E2E interactions |
| Sharing | Local / CI regression | External URL (Production or protected Preview) |
| Branching | `ds/*` | `prototype/*`, `experiment/*`, `concept/*` |

**ADR (summary):** Storybook = component validation environment. Prototype Lab = product workflow validation environment. See `docs/decisions.md` D006.

## 3. Folder structure

```text
src/
  components/ui/          # Design System (Storybook primary)
  prototype-shell/        # Hub + client router
    PrototypeIndex.tsx
    PrototypeRouter.tsx
  prototypes/
    registry.ts           # Prototype metadata
    <flow>/
      README.md
      pages/              # Route-level composition
      components/         # Flow-specific UI (not DS)
      mocks/              # Scenarios / fixtures
      state/              # Local state shape (storage-ready)
      analytics.ts        # Optional event stubs
```

## 4. Approved prototype lifecycle

```text
UX brief
  → prototype/* branch
  → Vercel Preview (protected)
  → external review (shareable bypass / share access; no repo required)
  → iteration
  → approval
  → merge main
  → Production Prototype Lab (public)
```

Implementation checklist:

1. **Branch** — `prototype/<flow-name>` (or `concept/<flow>-<variation>` for alternatives; `experiment/<name>` for DS usage experiments).
2. **Register** — add metadata in `src/prototypes/registry.ts`.
3. **Build** — page + mocks + local state; reuse `src/components/ui` only.
4. **Validate** — Hub + scenarios + Light/Dark + narrow viewport; `npm run build`.
5. **Share Preview** — Vercel Preview URL + reviewer bypass/share access (D008).
6. **Promote** — merge to `main` after approval; Production updates automatically. DS gaps go to decisions / backlog (do not invent tokens).

## 5. Branching and access model

| Prefix | Use | Deploy | Access |
|---|---|---|---|
| `main` | Stable approved Prototype Lab | **Production** | **Public** — portfolio / reusable flows |
| `prototype/*` | New workflow prototypes | **Preview** | **Protected** by default; externally shareable via bypass/share (reviewers need **not** have repo access) |
| `concept/*` | Alternative concepts / experiments | **Preview** | Same protected-review model as `prototype/*` |
| `experiment/*` | Time-boxed DS usage experiments | Optional Preview | Same Preview protection rules when deployed |
| `ds/*` | Design system components / tokens | Storybook / DS only | Not Prototype Lab sharing |

Example: `prototype/user-access-management`

### Production vs Preview

| Environment | Meaning |
|---|---|
| **Production** (`main`) | Stable/public prototype library |
| **Preview** (`prototype/*`, `concept/*`) | Work-in-progress / review environment |

**How deploys are created:** Vercel **Git integration** with the GitHub repo. Pushing `prototype/*` / `concept/*` opens Preview deployments; merging to `main` updates Production. Do not merge `prototype/*` to `main` before hosted Preview validation and approval.

One-time setup: [Import Git Repository](https://vercel.com/new) → select `olenakorin-ui/design-system-lab` → Framework Vite, Output `dist`, Build `npm run build`. Confirm `vercel.json` is picked up for SPA rewrites.

## 6. Scenario / mocking strategy

- One page implementation per flow.
- Scenarios live in `mocks/` and map to props / initial state.
- Select via query (`?scenario=viewer`) or in-page controls that update the URL.
- No duplicated page implementations per scenario.
- No backend, API, or auth in the lab unless a future decision says otherwise.

## 7. External sharing model

**Hosting:** Vercel  
**SPA config:** `vercel.json` rewrites non-asset paths to `/index.html` (D007).  
**Preview access:** Option C — protected Preview + shareable external access (D008).

1. `npm run build` produces a static SPA (`dist/`).
2. Deep links are first-class (hub, prototype routes, `?scenario=` variants).
3. Theme preference may persist in `localStorage` (`prototype-lab:theme`); flow state remains in-memory until a storage adapter is added.
4. **Production** is public (stable Prototype Lab).
5. **Preview** stays protected by default (SSO for default visitors).
6. **External reviewers** receive a shareable Protection Bypass URL (query `x-vercel-protection-bypass`, optional `x-vercel-set-bypass-cookie=true`) or dashboard Shareable Link / password. They must **not** need repository access. **Do not commit bypass secrets to git.**
7. Manage / rotate secrets: Vercel → Deployment Protection → Protection Bypass (`vercel project protection`).

**External reviewers must receive Prototype Lab URLs (Production or Preview+bypass), not Storybook URLs.**

## 8. Analytics

Prototype Lab ships **Vercel Web Analytics** and **Speed Insights** once at the application root (`src/App.tsx`), beside `PrototypeRouter`. Packages: `@vercel/analytics` and `@vercel/speed-insights` (React / Vite entrypoints — not Next.js).

Do **not** mount analytics inside individual prototypes, Design System components, or Storybook.

### Web Analytics

Automatic audience metrics (no custom `track` calls on Hobby):

- page views
- visitors
- bounce rate
- pages / routes
- hostnames
- referrers
- country
- device
- browser
- OS

### Speed Insights

Real-user performance metrics where available:

- LCP
- INP
- CLS
- FCP
- TTFB

### Plan limitation

**Custom events are not available on the current Vercel Hobby plan.** Do not add Pro-only analytics APIs, a second analytics provider, or product event wiring into UI components until a plan/decision change.
