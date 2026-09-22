# IMPLEMENTATION PLAN — Badge v0.1

Figma source: [Badge `26:169`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=26-169)

## Scope

Non-interactive semantic badge (`<span>`). Optional `asChild` for composition into interactive hosts.

## Figma inventory

- **Variants:** Default, Secondary, Outline, Destructive, Verified  
  — **no** success / warning / info
- **State:** Default, Hover, Focus (CSS only; not React props)
- Icons: optional left/right (12px), gap 4; Verified defaults with BadgeCheck metaphor via children
- Tokens: primary/secondary/outline/destructive recipes + `custom/blue-500-dark-blue-600` for Verified

## API

`variant`, `children`, `asChild`, `className`

## Stories

Variants, WithLeftIcon, WithRightIcon, LongLabel, DarkMode
