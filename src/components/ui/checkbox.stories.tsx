import type { Meta, StoryObj } from '@storybook/react-vite'
import React, { useId, useState } from 'react'

import { Checkbox } from '@/components/ui/checkbox'

const meta = {
  title: 'Components/Checkbox',
  component: Checkbox,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    disabled: { control: 'boolean' },
    checked: {
      control: 'select',
      options: [false, true, 'indeterminate'],
    },
  },
} satisfies Meta<typeof Checkbox>

export default meta
type Story = StoryObj<typeof meta>

function CheckboxField({
  label,
  description,
  long,
  ...checkboxProps
}: {
  label: string
  description?: string
  long?: boolean
} & React.ComponentProps<typeof Checkbox>) {
  const id = useId()
  const descriptionId = description ? `${id}-desc` : undefined
  return (
    <div className={`flex items-start gap-2 ${long ? 'w-[360px]' : 'w-[280px]'}`}>
      <Checkbox id={id} aria-describedby={descriptionId} className="mt-0.5" {...checkboxProps} />
      <div className="grid gap-1.5 leading-none">
        <label htmlFor={id} className="text-sm font-medium text-foreground cursor-pointer">
          {label}
        </label>
        {description && descriptionId ? (
          <p id={descriptionId} className="text-sm text-muted-foreground">
            {description}
          </p>
        ) : null}
      </div>
    </div>
  )
}

export const Unchecked: Story = {
  render: () => <Checkbox aria-label="Unchecked sample" />,
}

export const Checked: Story = {
  render: () => <Checkbox defaultChecked aria-label="Checked sample" />,
}

export const Indeterminate: Story = {
  render: () => <Checkbox checked="indeterminate" aria-label="Indeterminate sample" />,
}

export const DisabledIndeterminate: Story = {
  render: () => (
    <Checkbox checked="indeterminate" disabled aria-label="Disabled indeterminate" />
  ),
}

export const DisabledUnchecked: Story = {
  render: () => <Checkbox disabled aria-label="Disabled unchecked" />,
}

export const DisabledChecked: Story = {
  render: () => <Checkbox disabled defaultChecked aria-label="Disabled checked" />,
}

/** Tab to the control to verify focus-visible ring. */
export const FocusVisible: Story = {
  render: () => (
    <div className="flex flex-col gap-3">
      <p className="text-sm text-muted-foreground">Press Tab to focus the checkbox.</p>
      <Checkbox aria-label="Focus sample" />
    </div>
  ),
}

export const WithLabel: Story = {
  render: () => {
    const [checked, setChecked] = useState<boolean | 'indeterminate'>(false)
    return (
      <CheckboxField
        label="Checkbox Text"
        description="This is a checkbox description."
        checked={checked}
        onCheckedChange={(v) => setChecked(v === 'indeterminate' ? 'indeterminate' : v === true)}
      />
    )
  },
}

export const LongLabel: Story = {
  render: () => (
    <CheckboxField
      long
      label="I agree to the terms of service, privacy policy, and marketing communications for this product experience"
      description="You can change these preferences later in settings."
      defaultChecked
    />
  ),
}

export const DarkMode: Story = {
  globals: { theme: 'dark' },
  render: () => (
    <div className="flex flex-col gap-4">
      <CheckboxField label="Checked" description="Dark mode checked." defaultChecked />
      <CheckboxField
        label="Indeterminate"
        description="Dark mode mixed selection."
        checked="indeterminate"
      />
    </div>
  ),
}
