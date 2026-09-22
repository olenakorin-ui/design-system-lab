# IMPLEMENTATION PLAN — Select v0.1

Figma: [Select `345:11530`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=345-11530), [Select Menu / Item `118:1541`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=118-1541), [Select / Menu `118:2501`](https://www.figma.com/design/ZllxQplWi5QJcNeUHeY8T3/Design-System-V2?node-id=118-2501)

## Scope

Radix Select control (trigger + content + items). Label/description composed in stories.

## Figma

- Trigger states: Default, Focus, Filled, Filled (Focus), Disabled
- Menu: `popover` fill, `border` stroke, radius md
- Item: Default / Hover (`accent`); Checkbox variant deferred (not required for sprint)

## API

`Select`, `SelectTrigger`, `SelectValue`, `SelectContent`, `SelectItem`, `SelectGroup`, `SelectLabel`, `SelectSeparator`
