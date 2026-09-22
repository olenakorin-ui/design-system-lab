import type { Meta, StoryObj } from '@storybook/react-vite'
import { ArrowRight, BadgeCheck, Check } from 'lucide-react'

import { Badge } from '@/components/ui/badge'

const meta = {
  title: 'Components/Badge',
  component: Badge,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'secondary', 'outline', 'destructive', 'verified'],
    },
  },
} satisfies Meta<typeof Badge>

export default meta
type Story = StoryObj<typeof meta>

export const Variants: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Badge variant="default">Badge</Badge>
      <Badge variant="secondary">Badge</Badge>
      <Badge variant="outline">Badge</Badge>
      <Badge variant="destructive">Badge</Badge>
      <Badge variant="verified">
        <BadgeCheck aria-hidden="true" />
        Verified
      </Badge>
    </div>
  ),
}

export const WithLeftIcon: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Badge>
        <Check aria-hidden="true" />
        Badge
      </Badge>
      <Badge variant="secondary">
        <Check aria-hidden="true" />
        Badge
      </Badge>
      <Badge variant="outline">
        <Check aria-hidden="true" />
        Badge
      </Badge>
    </div>
  ),
}

export const WithRightIcon: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Badge>
        Badge
        <ArrowRight aria-hidden="true" />
      </Badge>
      <Badge variant="destructive">
        Badge
        <ArrowRight aria-hidden="true" />
      </Badge>
    </div>
  ),
}

export const LongLabel: Story = {
  args: {
    children: 'A longer badge label that still should stay on one line when possible',
  },
}

export const DarkMode: Story = {
  globals: { theme: 'dark' },
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Badge variant="default">Badge</Badge>
      <Badge variant="secondary">Badge</Badge>
      <Badge variant="outline">Badge</Badge>
      <Badge variant="destructive">Badge</Badge>
      <Badge variant="verified">
        <BadgeCheck aria-hidden="true" />
        Verified
      </Badge>
    </div>
  ),
}
