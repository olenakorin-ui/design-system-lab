import type { Meta, StoryObj } from '@storybook/react-vite'
import { useId, useState } from 'react'

import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'

const meta = {
  title: 'Components/Select',
  component: Select,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
} satisfies Meta<typeof Select>

export default meta
type Story = StoryObj<typeof meta>

const fruits = [
  'Apple',
  'Banana',
  'Blueberry',
  'Grapes',
  'Pineapple',
  'Strawberry',
  'Watermelon',
]

function SelectField({
  label,
  description,
  disabled,
  placeholder = 'Placeholder',
  defaultValue,
  many,
  longOptions,
}: {
  label: string
  description?: string
  disabled?: boolean
  placeholder?: string
  defaultValue?: string
  many?: boolean
  longOptions?: boolean
}) {
  const id = useId()
  const descriptionId = description ? `${id}-desc` : undefined
  const [value, setValue] = useState(defaultValue)
  const options = many
    ? Array.from({ length: 24 }, (_, i) => `Option ${i + 1}`)
    : longOptions
      ? [
          'A particularly long option label that should truncate or wrap carefully',
          'Another extremely verbose choice for overflow testing',
          'Short',
        ]
      : fruits

  return (
    <div className="flex w-[280px] flex-col gap-2">
      <label htmlFor={id} className="text-sm font-medium text-foreground">
        {label}
      </label>
      <Select value={value} onValueChange={setValue} disabled={disabled}>
        <SelectTrigger id={id} aria-describedby={descriptionId}>
          <SelectValue placeholder={placeholder} />
        </SelectTrigger>
        <SelectContent>
          <SelectGroup>
            <SelectLabel>Options</SelectLabel>
            {options.map((opt) => (
              <SelectItem key={opt} value={opt.toLowerCase().replace(/\s+/g, '-')}>
                {opt}
              </SelectItem>
            ))}
          </SelectGroup>
        </SelectContent>
      </Select>
      {description && descriptionId ? (
        <p id={descriptionId} className="text-sm text-muted-foreground">
          {description}
        </p>
      ) : null}
    </div>
  )
}

export const Default: Story = {
  render: () => (
    <SelectField label="Fruit" description="This is a select description." />
  ),
}

export const WithValue: Story = {
  render: () => (
    <SelectField label="Fruit" defaultValue="banana" description="Pre-selected value." />
  ),
}

export const Placeholder: Story = {
  render: () => <SelectField label="Fruit" placeholder="Choose a fruit…" />,
}

export const Disabled: Story = {
  render: () => (
    <SelectField label="Fruit" disabled defaultValue="apple" description="Editing locked." />
  ),
}

export const OpenState: Story = {
  render: () => (
    <div className="flex flex-col gap-3 pb-64">
      <p className="text-sm text-muted-foreground">Click the trigger to open the menu.</p>
      <SelectField label="Fruit" />
    </div>
  ),
}

export const LongOptions: Story = {
  render: () => <SelectField label="Choice" longOptions />,
}

export const ManyOptions: Story = {
  render: () => <SelectField label="Many" many description="Scroll the list." />,
}

export const DarkMode: Story = {
  globals: { theme: 'dark' },
  render: () => (
    <SelectField label="Fruit" defaultValue="apple" description="Dark mode select." />
  ),
}
