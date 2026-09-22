# IMPLEMENTATION PLAN — Dialog v0.1

Figma: [Dialog `112:602`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=112-602)

- Breakpoints lg/sm (responsive padding/layout via CSS, not React props)
- Panel: `background` + `border`, radius lg
- Title `foreground`, Description `muted-foreground`
- Close icon; Footer with cancel/primary actions (compose Button)
- No overlay node in component set — use standard dimmed overlay (`black/80`)

API: Radix Dialog parts + Header/Footer helpers
