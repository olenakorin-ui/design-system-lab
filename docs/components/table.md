# Table — Figma ↔ code parity (v0.2 foundation)

Figma: [Table `184:890`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=184-890), [Data Table `244:2897`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=244-2897)  
Code: `src/components/ui/table.tsx`  
Stories: `src/components/ui/table.stories.tsx`

## Scope

**Foundation only** — semantic table primitives. Not a DataGrid.

Out of scope: sorting system, column resize, virtualisation, server pagination, column visibility, drag/drop.

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
| Rounded table chrome | Optional outer border via consumer; foundation uses scroll wrapper |

## Responsive behavior (Sprint 1)

**Default implemented: horizontal scroll** (`overflow-x-auto` on container), matching Figma `overflow-clip` / min-width dense tables.

```text
DECISION REQUIRED
- Question: Table narrow viewport — horizontal scroll vs stacked mobile rows?
- Why it matters: Global responsive rule affects all admin directories.
- Option A: Horizontal scroll (current foundation default)
- Option B: Stacked mobile rows (card-like)
- Technical implications: A preserves column alignment; B needs a separate layout recipe and may not use native table semantics on small screens.
```

## Stories

Default, Selectable, SelectedRows, LongContent, ManyRows, Empty, NarrowViewport, DarkMode

## Accessibility

Semantic `<table>` / header cells; row selection via labelled checkboxes; keyboard focus on interactive cell contents (Checkbox, DropdownMenu trigger).

## Known differences

1. Data Table playground also includes filters + pagination chrome — deferred (Pagination P1).
2. Sortable head “Button” pattern deferred (no sorting system this sprint).
3. Cell size variants (md/lg) and Badge/Avatar/Switch cell variants deferred — compose existing components.
