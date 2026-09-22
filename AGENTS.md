# Design System Agent Rules

When creating or editing UI in this repository:

1. Reuse an existing design-system component before creating a new one.
2. Use semantic tokens; do not hardcode product colors inside components.
3. Do not replace semantic tokens with raw primitive values in product UI.
4. Preserve light and dark mode behavior.
5. Keep Figma-facing component names and code-facing APIs conceptually aligned.
6. Preserve keyboard behavior, visible focus, accessible names, and contrast.
7. Treat loading, empty, disabled, error, hover, focus, and selected states as first-class states where relevant.
8. Do not create a new component variant until checking whether an existing prop/state can represent the need.
9. Update Storybook stories when component behavior or states change.
10. Do not silently change token meaning. Document semantic-token changes in the decision log.


11. Treat `tokens/*.tokens.json` as the canonical token source, extracted from Figma Design System V2. Keep CSS mappings synchronized with those files.
12. Use `border` for low-emphasis structural separation and `input` / `border-strong` when a UI control boundary needs stronger visibility.
13. Prefer semantic status tokens (success, warning, destructive, info) over direct status primitives in product components.
