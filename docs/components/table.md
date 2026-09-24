# Table — Figma ↔ code parity (v0.2 foundation)

Figma: [Table `184:890`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=184-890), [Data Table `244:2897`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=244-2897)  
Code: `src/components/ui/table.tsx`  
Stories: `src/components/ui/table.stories.tsx`  
Decision: **D009** — narrow viewport horizontal scroll

## Scope

**Foundation only** — semantic table primitives. Not a DataGrid.

Out of scope: sorting system, column resize, virtualisation, server pagination, column visibility, drag/drop, stacked/card mobile layouts, `responsive="cards"` (or equivalent) on the core API.

## API

| Export | Element |
|---|---|
| `Table` | Wrapper (`overflow-x-auto`) + `<table>` |
| `TableHeader` | `<thead>` |
| `TableBody` | `<tbody>` |
| `TableFooter` | `<tfoot>` (supported for composition; Figma caption/footer pattern) |
| `TableRow` | `<tr>` (`data-state=selected` supported) |
| `TableHead` | `<th>` |
| `TableCell` | `<td>` |
| `TableCaption` | `<caption>` |

Compose with existing `Checkbox`, `Badge`, `DropdownMenu`, `Button`.

## Figma → code

| Figma | Code |
|---|---|
| Cell / head bottom border | `border-b border-border` on rows |
| Head text muted | `text-muted-foreground font-medium` |
| Cell text | `text-foreground` (inherit) |
| Caption | `text-muted-foreground text-sm` |
| Checkbox / action cells | Composition in stories |
| min-width / overflow | Horizontal scroll wrapper; Figma min-width / overflow is the visual baseline |
| Rounded table chrome | Optional outer border via consumer; foundation uses scroll wrapper |

## Responsive behavior (global DS rule)

Base Table **preserves native table structure across breakpoints**.

| Viewport | Behavior |
|---|---|
| **Wide** | Native `<table>` — columns visible in place |
| **Narrow** | Same native `<table>` — **horizontal scroll** when content exceeds available width |

When table content exceeds the available viewport:

- keep native `<table>` semantics
- preserve columns
- use horizontal overflow (`overflow-x-auto` on the container)
- do **not** automatically convert rows into cards
- do **not** automatically hide columns
- do **not** create duplicate mobile markup

Figma’s current min-width / overflow behavior remains the baseline (**D009**).

### Stacked mobile rows

Stacked / card-like mobile rows are a **separate product/layout pattern**, not part of the Table foundation.

Do **not** add `responsive="cards"` (or equivalent) to the core Table API in v0.2. If future prototype evidence requires stacked mobile data presentation, record it as a separate pattern/component investigation (see backlog).

## Acceptance / validation

| Check | How |
|---|---|
| No clipping of cells/chrome | Scroll container; `NarrowViewport` story |
| Selection usable when scrolled | Checkbox composition in `NarrowViewport` / `Selectable` |
| Row actions reachable | Dropdown Menu trigger in `NarrowViewport` |
| Long content | `LongContent` + narrow scroll |
| Keyboard focus inside scrolled content | Tab to Checkbox / Menu trigger inside scrollport |
| Light / Dark | Default + `DarkMode` |
| Narrow Storybook viewport | `NarrowViewport` (`mobile1`) |

## Stories

Default, Selectable, SelectedRows, LongContent, ManyRows, Empty, NarrowViewport, DarkMode

## Accessibility

Semantic `<table>` / header cells; row selection via labelled checkboxes; keyboard focus on interactive cell contents (Checkbox, DropdownMenu trigger) remains available while the table scrolls horizontally.

## Known differences

1. Data Table playground also includes filters + pagination chrome — deferred (Pagination P1).
2. Sortable head “Button” pattern deferred (no sorting system this sprint).
3. Cell size variants (md/lg) and Badge/Avatar/Switch cell variants deferred — compose existing components.
4. Stacked mobile data layout — deferred as a separate pattern (not Table API).
