# Design System Token Specification v0.1

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

Raw primitive values are intentionally TBD until the visual direction is selected.

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
Temporary implementation font: Inter until brand typography is selected.

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
Working scale; validate after visual direction is selected.
- radius/none = 0
- radius/sm = 6px
- radius/md = 8px
- radius/lg = 10px
- radius/xl = 14px
- radius/2xl = 18px
- radius/full = 9999px

## Shadows
- shadow/xs: subtle 1px elevation/border replacement
- shadow/sm: low-elevation floating surface
- shadow/md: menus/popovers
- shadow/lg: dialogs/large overlays

Exact values remain TBD until component visual QA.

## Motion
- duration/fast = 100ms
- duration/normal = 150ms
- duration/moderate = 200ms
- duration/slow = 300ms
- easing/standard = cubic-bezier(0.2, 0, 0, 1)
- easing/emphasized = cubic-bezier(0.2, 0, 0, 1)

## Figma mapping
Recommended collections:
1. Primitives — Value mode
2. Color — Light / Dark modes
3. Spacing — Value mode
4. Radius — Value mode

Every semantic Figma color variable should alias a primitive variable and receive matching web code syntax, e.g. `var(--primary)`.

## Component rule
No component is added to the v0.1 library until:
- semantic tokens it needs exist;
- light/dark behavior is defined;
- focus/disabled/error behavior is understood;
- code API and Figma property model can be aligned.
