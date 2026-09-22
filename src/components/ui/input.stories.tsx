import type { Meta, StoryObj } from '@storybook/react-vite'
import React, { useId } from 'react'

import { Input } from '@/components/ui/input'

const meta = {
  title: 'Components/Input',
  component: Input,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    disabled: { control: 'boolean' },
    invalid: { control: 'boolean' },
    placeholder: { control: 'text' },
    type: {
      control: 'select',
      options: ['text', 'email', 'password', 'search', 'file'],
    },
  },
} satisfies Meta<typeof Input>

export default meta
type Story = StoryObj<typeof meta>

function FieldShell({
  label,
  description,
  children,
}: {
  label: string
  description?: string
  children: (ids: { inputId: string; descriptionId?: string }) => React.ReactNode
}) {
  const inputId = useId()
  const descriptionId = description ? `${inputId}-desc` : undefined
  return (
    <div className="flex w-[320px] flex-col gap-2">
      <label htmlFor={inputId} className="text-sm font-medium text-foreground">
        {label}
      </label>
      {children({ inputId, descriptionId })}
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
    <FieldShell label="Email" description="We will never share your email.">
      {({ inputId, descriptionId }) => (
        <Input
          id={inputId}
          name="email"
          type="email"
          placeholder="you@example.com"
          aria-describedby={descriptionId}
        />
      )}
    </FieldShell>
  ),
}

export const WithValue: Story = {
  render: () => (
    <FieldShell label="Name">
      {({ inputId }) => (
        <Input id={inputId} name="name" defaultValue="Ada Lovelace" />
      )}
    </FieldShell>
  ),
}

export const Placeholder: Story = {
  render: () => (
    <FieldShell label="Search">
      {({ inputId }) => (
        <Input id={inputId} name="q" type="search" placeholder="Search projects…" />
      )}
    </FieldShell>
  ),
}

export const Disabled: Story = {
  render: () => (
    <FieldShell label="Username" description="Editing is locked.">
      {({ inputId, descriptionId }) => (
        <Input
          id={inputId}
          name="username"
          defaultValue="olenakorin"
          disabled
          aria-describedby={descriptionId}
        />
      )}
    </FieldShell>
  ),
}

export const Invalid: Story = {
  render: () => (
    <FieldShell label="Email" description="Enter a valid email address.">
      {({ inputId, descriptionId }) => (
        <Input
          id={inputId}
          name="email"
          type="email"
          defaultValue="not-an-email"
          invalid
          aria-describedby={descriptionId}
        />
      )}
    </FieldShell>
  ),
}

/** Tab into the field to verify focus-visible ring. */
export const FocusVisible: Story = {
  render: () => (
    <FieldShell label="Focus me" description="Press Tab to move focus onto the input.">
      {({ inputId, descriptionId }) => (
        <Input
          id={inputId}
          name="focus"
          placeholder="Tab here"
          aria-describedby={descriptionId}
        />
      )}
    </FieldShell>
  ),
}

export const LongValue: Story = {
  render: () => (
    <FieldShell label="Title">
      {({ inputId }) => (
        <Input
          id={inputId}
          name="title"
          defaultValue="A particularly long value that should truncate or scroll within the field without breaking layout"
        />
      )}
    </FieldShell>
  ),
}

export const DarkMode: Story = {
  globals: {
    theme: 'dark',
  },
  render: () => (
    <FieldShell label="Email" description="Dark mode field chrome.">
      {({ inputId, descriptionId }) => (
        <Input
          id={inputId}
          name="email"
          type="email"
          placeholder="you@example.com"
          aria-describedby={descriptionId}
        />
      )}
    </FieldShell>
  ),
}
