# Prototype architecture

## 1. Purpose

Separate **Design System component validation** from **product workflow validation**.

- **Storybook** = Design System component validation only (docs, states, Figma parity, a11y, regression).
- **Prototype Lab** = product-flow runtime (pages, mocks, scenarios, external sharing).

## 2. Storybook vs Prototype Lab

| | Storybook | Prototype Lab |
|---|---|---|
| Audience | Design system authors / implementers | Product / UX / stakeholders |
| Content | Components, states, Figma parity, a11y | Pages, flows, mocked data, E2E interactions |
| Sharing | Local / CI regression | External URL (when deployed) |
| Branching | `ds/*` | `prototype/*`, `experiment/*`, `concept/*` |

**ADR (summary):** Storybook = component validation environment. Prototype Lab = product workflow validation environment. See `docs/decisions.md` D006.

**Stable vs preview (after lab-shell on `main`):**

- `main` = stable Prototype Lab (Vercel Production)
- `prototype/*` = new workflow previews
- `concept/*` = alternative concept previews
- Storybook = DS component validation only (not the sharing surface)

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

## 4. Prototype lifecycle

1. **Branch** — `prototype/<flow-name>` (or `experiment/<name>` for DS usage experiments).
2. **Register** — add metadata in `src/prototypes/registry.ts`.
3. **Build** — page + mocks + local state; reuse `src/components/ui` only.
4. **Validate** — Hub + scenarios + Light/Dark + narrow viewport; `npm run build`.
5. **Share** — deploy Prototype Lab build (host SPA fallback required for deep links).
6. **Promote** — approved reusable flows may merge to `main`; DS gaps go to decisions / backlog (do not invent tokens).

## 5. Branching model

| Prefix | Use |
|---|---|
| `ds/<task>` | Design system components / tokens |
| `prototype/<flow-name>` | Durable product flow prototypes |
| `experiment/<name>` | Time-boxed DS usage experiments |
| `concept/<flow>-<variation>` | Exploratory alternatives |

Example: `prototype/user-access-management`

### Deployment mapping (Vercel)

| Git ref | Deployment |
|---|---|
| `main` | Stable Prototype Lab (production) |
| `prototype/*` | Preview deployments for new flows |
| `concept/*` | Preview deployments for alternative concepts |
| `experiment/*` | Optional previews for DS usage experiments |

**How previews are created:** Vercel **Git integration** with the GitHub repo (dashboard import). Pushing `prototype/*` / `concept/*` opens preview deployments; `main` is production. Do not merge `prototype/*` to `main` before hosted validation.

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
**Preview access:** Protected + shareable bypass (D008).

1. `npm run build` produces a static SPA (`dist/`).
2. Deep links are first-class (hub, prototype routes, `?scenario=` variants).
3. Theme preference may persist in `localStorage` (`prototype-lab:theme`); flow state remains in-memory until a storage adapter is added.
4. **Default Preview access** requires Vercel authentication (SSO).
5. **External reviewers** get a shareable link that includes the project **Protection Bypass** secret (query `x-vercel-protection-bypass`, optional `x-vercel-set-bypass-cookie=true`), or a dashboard Shareable Link / password if the team switches to that mechanism. **Do not commit bypass secrets to git.**
6. Manage / rotate secrets in the Vercel project: Deployment Protection → Protection Bypass (CLI: `vercel project protection`).

**External reviewers must receive Prototype Lab URLs (with bypass when needed), not Storybook URLs.**

Storybook remains the Design System validation environment (components, Figma parity, a11y). Prototype Lab remains the product-flow runtime and sharing surface.
