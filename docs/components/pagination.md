# Pagination — Figma ↔ code parity (v0.2)

Figma: [Pagination `208:1701`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=208-1701), [PaginationItem `208:1651`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=208-1651)  
Code: `src/components/ui/pagination.tsx`  
Stories: `src/components/ui/pagination.stories.tsx`

## Scope

UI foundation for paged navigation. **No** server-fetch API, page-size logic, infinite scroll, or product total-count helpers.

## API

| Export | Role |
|---|---|
| `Pagination` | `<nav aria-label="Pagination">` |
| `PaginationContent` | `<ul>` |
| `PaginationItem` | `<li>` |
| `PaginationLink` | Page control; `isActive` → `aria-current="page"` + outline |
| `PaginationPrevious` / `PaginationNext` | Labeled controls (disable at boundaries) |
| `PaginationEllipsis` | Figma-supported ellipsis (decorative + sr-only) |

## Figma → code

| Figma | Code |
|---|---|
| Previous / Next ghost + chevron | `PaginationPrevious` / `PaginationNext` via `Button variant="ghost"` |
| Link default | Ghost icon button |
| Link active | Outline + `aria-current="page"` |
| Hover / focus | Button CSS (`accent` hover, `--custom-outline` focus) |
| Disabled | `disabled` + opacity via Button |
| Ellipsis | `PaginationEllipsis` (`MoreHorizontal`) |

## Stories

FirstPage, MiddlePage, LastPage, ManyPages, DarkMode

## Accessibility

Nav landmark; current page announced; Previous/Next `aria-label`s in stories; disabled boundaries prevent activation.

## Known differences

1. Active visual uses existing `Button` outline recipe (border + custom input fill) rather than inventing a pagination-only surface.
2. Page list composition (which numbers to show) is consumer/story responsibility — not a DS algorithm.
