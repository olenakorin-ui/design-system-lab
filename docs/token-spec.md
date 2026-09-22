# Design System Token Specification v0.3

## Principles
- Repository is the durable source layer.
- Figma Variables mirror repository token names and semantics.
- Components consume semantic tokens, not raw color primitives.
- Light/dark mode changes semantic mappings, not component APIs.
- Token names describe purpose before appearance.

## Color architecture

### Primitive collections
- neutral/0, 50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950
- brand/50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950
- red/50...950
- amber/50...950
- green/50...950
- blue/50...950

Canonical primitive values come from Figma collection `1. TailwindCSS`. See v0.3 below.

### Semantic color tokens
Core shadcn-compatible tokens:
- background / foreground
- card / card-foreground
- popover / popover-foreground
- primary / primary-foreground
- secondary / secondary-foreground
- muted / muted-foreground
- accent / accent-foreground
- destructive / destructive-foreground
- border
- input
- ring

Additional system tokens:
- success / success-foreground
- warning / warning-foreground
- info / info-foreground
- surface-raised
- surface-sunken
- border-strong
- focus-ring

Modes: Light, Dark.

## Typography
Implementation font from Figma Theme: Geist (sans), Georgia (serif), Geist Mono (mono).

Suggested semantic styles:
- display-lg: 48/56, 600
- heading-1: 36/44, 600
- heading-2: 30/38, 600
- heading-3: 24/32, 600
- heading-4: 20/28, 600
- body-lg: 16/24, 400
- body-md: 14/20, 400
- body-sm: 12/16, 400
- label-md: 14/20, 500
- label-sm: 12/16, 500
- code: 13/20, 400 monospace

## Spacing
- space/0 = 0
- space/1 = 4px
- space/2 = 8px
- space/3 = 12px
- space/4 = 16px
- space/5 = 20px
- space/6 = 24px
- space/8 = 32px
- space/10 = 40px
- space/12 = 48px
- space/16 = 64px

## Radius
From Figma Theme / radius:
- radius/none = 0
- radius/xs = 2px
- radius/sm = 6px
- radius/md = 8px
- radius/lg = 10px
- radius/xl = 14px
- radius/2xl = 16px
- radius/3xl = 24px
- radius/4xl = 32px
- radius/full = 9999px

## Shadows
- shadow/xs: subtle 1px elevation/border replacement
- shadow/sm: low-elevation floating surface
- shadow/md: menus/popovers
- shadow/lg: dialogs/large overlays

Canonical shadow values live in `/tokens/shadow.tokens.json` (Figma Theme / shadow).

## Motion
- duration/fast = 100ms
- duration/normal = 150ms
- duration/moderate = 200ms
- duration/slow = 300ms
- easing/standard = cubic-bezier(0.2, 0, 0, 1)
- easing/emphasized = cubic-bezier(0.2, 0, 0, 1)

## Figma mapping
Design System V2 collections:
1. `1. TailwindCSS` — Default mode (primitives: spacing, radius, Tailwind color scales)
2. `2. Theme` — Default mode (semantic light/dark color pairs, type, shadow)
3. `3. Mode` — Light / Dark modes (component-facing aliases)
4. `4. Custom` — Desktop / Mobile modes (heading and section layout)

Every semantic Figma color variable should alias a primitive variable and receive matching web code syntax, e.g. `var(--primary)`.

## Component rule
No component is added to the v0.1 library until:
- semantic tokens it needs exist;
- light/dark behavior is defined;
- focus/disabled/error behavior is understood;
- code API and Figma property model can be aligned.


---

## Color tokens v0.2 — Cool-neutral + Indigo/Violet

Canonical file: `/tokens/color.tokens.json`  
CSS mirror: `/src/styles/tokens.css`

### Neutral palette

| Token | Hex |
|---|---|
| neutral/0 | #FFFFFF |
| neutral/50 | #F8FAFC |
| neutral/100 | #F1F4F9 |
| neutral/200 | #E3E8F0 |
| neutral/300 | #CCD4E0 |
| neutral/400 | #8996A7 |
| neutral/500 | #68758A |
| neutral/600 | #4B576A |
| neutral/700 | #364153 |
| neutral/800 | #232C3A |
| neutral/900 | #151C28 |
| neutral/950 | #0B1018 |

### Brand palette

| Token | Hex |
|---|---|
| brand/50 | #F7F5FF |
| brand/100 | #EFEAFF |
| brand/200 | #E0D7FF |
| brand/300 | #C9B8FF |
| brand/400 | #AD92FF |
| brand/500 | #8F6BF8 |
| brand/600 | #7353F3 |
| brand/700 | #5E3FD7 |
| brand/800 | #4B33AD |
| brand/900 | #3E2D87 |
| brand/950 | #24184F |

Status primitives use green, amber, red, and blue scales. See the canonical token file for complete values.

### Light semantic mapping

| Semantic token | Primitive |
|---|---|
| background | neutral/0 |
| foreground | neutral/950 |
| card | neutral/0 |
| card-foreground | neutral/950 |
| primary | brand/600 |
| primary-foreground | neutral/0 |
| secondary | neutral/100 |
| secondary-foreground | neutral/900 |
| muted | neutral/100 |
| muted-foreground | neutral/600 |
| accent | brand/50 |
| accent-foreground | brand/800 |
| destructive | red/600 |
| destructive-foreground | neutral/0 |
| border | neutral/200 |
| border-strong | neutral/400 |
| input | neutral/400 |
| ring / focus-ring | brand/500 |
| surface-raised | neutral/0 |
| surface-sunken | neutral/50 |

### Dark semantic mapping

| Semantic token | Primitive |
|---|---|
| background | neutral/950 |
| foreground | neutral/50 |
| card | neutral/900 |
| card-foreground | neutral/50 |
| primary | brand/400 |
| primary-foreground | neutral/950 |
| secondary | neutral/800 |
| secondary-foreground | neutral/50 |
| muted | neutral/800 |
| muted-foreground | neutral/400 |
| accent | brand/900 |
| accent-foreground | brand/100 |
| destructive | red/400 |
| destructive-foreground | neutral/950 |
| border | neutral/800 |
| border-strong | neutral/600 |
| input | neutral/500 |
| ring / focus-ring | brand/400 |
| surface-raised | neutral/900 |
| surface-sunken | neutral/950 |

### Status semantics

Each status supports both a solid pair and a subtle pair:

- success / success-foreground / success-subtle / success-subtle-foreground
- warning / warning-foreground / warning-subtle / warning-subtle-foreground
- destructive / destructive-foreground / error-subtle / error-subtle-foreground
- info / info-foreground / info-subtle / info-subtle-foreground

### Contrast audit

Initial WCAG contrast checks:

| Pair | Ratio |
|---|---:|
| Light foreground / background | 19.06:1 |
| Light muted foreground / background | 7.32:1 |
| Light primary foreground / primary | 4.93:1 |
| Light destructive foreground / destructive | 4.83:1 |
| Light accent foreground / accent | 8.19:1 |
| Dark foreground / background | 18.22:1 |
| Dark muted foreground / background | 6.34:1 |
| Dark primary foreground / primary | 7.56:1 |
| Dark destructive foreground / destructive | 6.89:1 |
| Dark accent foreground / accent | 9.27:1 |
| Light focus ring / background | 3.73:1 |
| Dark focus ring / background | 7.56:1 |
| Light interactive input border / white background | 3.01:1 |

Notes:
- Decorative borders may intentionally use lower contrast than interactive boundaries.
- `input` is mapped to a stronger neutral than `border` so form controls remain identifiable.
- These checks validate token pairs, not every future component state. Component-level QA is still required.

---

## Color tokens v0.3 — Extracted from Design System V2

Source: [Design System V2](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=580-9181)  
Canonical files: `/tokens/*.tokens.json`  
CSS mirror: `/src/styles/tokens.css`

This replaces the v0.2 cool-neutral + indigo/violet placeholder with the Figma shadcn/ui variable set. See D003.

### Neutral palette (Tailwind Neutral)

| Token | Hex |
|---|---|
| white / neutral/0 | #FFFFFF |
| neutral/50 | #FAFAFA |
| neutral/100 | #F5F5F5 |
| neutral/200 | #E5E5E5 |
| neutral/300 | #D4D4D4 |
| neutral/400 | #A3A3A3 |
| neutral/500 | #737373 |
| neutral/600 | #525252 |
| neutral/700 | #404040 |
| neutral/800 | #262626 |
| neutral/900 | #171717 |
| neutral/950 | #0A0A0A |

`brand/*` aliases `blue/*`. Full Tailwind palettes (slate through rose) are in the canonical color file.

### Light Mode mapping

| Semantic token | Figma alias |
|---|---|
| background | white |
| foreground | neutral/950 |
| card | white |
| primary | blue/600 |
| primary-foreground | neutral/50 |
| secondary / muted / accent | neutral/100 |
| muted-foreground | neutral/500 |
| destructive | red/600 |
| destructive-foreground | red/50 |
| border / input | neutral/200 |
| ring | neutral/400 |
| sidebar | neutral/50 |
| sidebar-primary | neutral/900 |

### Dark Mode mapping

| Semantic token | Figma alias |
|---|---|
| background | neutral/950 |
| foreground | neutral/50 |
| card | neutral/900 |
| popover | neutral/800 |
| primary | neutral/200 |
| primary-foreground | neutral/900 |
| secondary / muted | neutral/800 |
| accent | neutral/700 |
| destructive | red/400 |
| border | white @ 10% |
| input | white @ 15% |
| ring | neutral/500 |
| sidebar | neutral/900 |
| sidebar-primary | blue/700 |

### Additional Figma tokens

- Chart: `chart-1` … `chart-5` (mode-aware)
- Sidebar: `sidebar`, `sidebar-foreground`, `sidebar-primary`, `sidebar-accent`, `sidebar-border`, `sidebar-ring`
- Alpha overlays: `alpha/5` … `alpha/90`
- Type: Geist / Georgia / Geist Mono, `text/xs` … `text/9xl`
- Radius: none, xs, sm, md, lg, xl, 2xl, 3xl, 4xl, full
- Shadow: 2xs, xs, sm, md, lg, xl, 2xl

Lab extensions kept on top of Figma: `success`, `warning`, `info`, `border-strong`, `surface-raised`, `surface-sunken`.
