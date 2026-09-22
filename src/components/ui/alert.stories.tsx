import type { Meta, StoryObj } from '@storybook/react-vite'
import { CircleAlert, CircleCheck } from 'lucide-react'

import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'

const meta = {
  title: 'Components/Alert',
  component: Alert,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
  argTypes: {
    variant: { control: 'select', options: ['default', 'destructive'] },
  },
} satisfies Meta<typeof Alert>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: () => (
    <Alert className="w-[520px]">
      <CircleCheck aria-hidden="true" />
      <AlertTitle>Alert Title</AlertTitle>
      <AlertDescription>This is an alert description.</AlertDescription>
    </Alert>
  ),
}

export const Destructive: Story = {
  render: () => (
    <Alert variant="destructive" className="w-[520px]">
      <CircleAlert aria-hidden="true" />
      <AlertTitle>Alert Title</AlertTitle>
      <AlertDescription>This is an alert description.</AlertDescription>
    </Alert>
  ),
}

export const TitleOnly: Story = {
  render: () => (
    <Alert className="w-[520px]">
      <CircleCheck aria-hidden="true" />
      <AlertTitle>Alert Title</AlertTitle>
    </Alert>
  ),
}

export const DescriptionOnly: Story = {
  render: () => (
    <Alert className="w-[520px]">
      <AlertDescription>This is an alert description without a title.</AlertDescription>
    </Alert>
  ),
}

export const WithIcon: Story = {
  render: () => (
    <Alert className="w-[520px]">
      <CircleCheck aria-hidden="true" />
      <AlertTitle>Heads up</AlertTitle>
      <AlertDescription>You can compose any decorative icon as a child.</AlertDescription>
    </Alert>
  ),
}

export const LongContent: Story = {
  render: () => (
    <Alert className="w-[520px]">
      <CircleCheck aria-hidden="true" />
      <AlertTitle>A longer alert title that may need to truncate carefully</AlertTitle>
      <AlertDescription>
        This description is intentionally long to validate wrapping, spacing, and readability across
        multiple lines without inventing additional layout tokens or status variants.
      </AlertDescription>
    </Alert>
  ),
}

export const DarkMode: Story = {
  globals: { theme: 'dark' },
  render: () => (
    <div className="flex w-[520px] flex-col gap-4">
      <Alert>
        <CircleCheck aria-hidden="true" />
        <AlertTitle>Alert Title</AlertTitle>
        <AlertDescription>Dark mode default alert.</AlertDescription>
      </Alert>
      <Alert variant="destructive">
        <CircleAlert aria-hidden="true" />
        <AlertTitle>Alert Title</AlertTitle>
        <AlertDescription>Dark mode destructive alert.</AlertDescription>
      </Alert>
    </div>
  ),
}
