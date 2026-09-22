import type { Meta, StoryObj } from '@storybook/react-vite'
import { Circle, Plus } from 'lucide-react'

import { Button } from '@/components/ui/button'

const meta = {
  title: 'Components/Button',
  component: Button,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'secondary', 'destructive', 'outline', 'ghost', 'link'],
    },
    size: {
      control: 'select',
      options: ['default', 'sm', 'lg', 'icon'],
    },
    disabled: { control: 'boolean' },
    loading: { control: 'boolean' },
  },
} satisfies Meta<typeof Button>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    children: 'Button',
  },
}

export const Variants: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Button variant="default">Default</Button>
      <Button variant="secondary">Secondary</Button>
      <Button variant="destructive">Destructive</Button>
      <Button variant="outline">Outline</Button>
      <Button variant="ghost">Ghost</Button>
      <Button variant="link">Link</Button>
    </div>
  ),
}

export const Sizes: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Button size="sm">Small</Button>
      <Button size="default">Default</Button>
      <Button size="lg">Large</Button>
      <Button size="icon" aria-label="Add">
        <Plus />
      </Button>
    </div>
  ),
}

export const Disabled: Story = {
  args: {
    children: 'Disabled',
    disabled: true,
  },
}

export const Loading: Story = {
  args: {
    children: 'Loading',
    loading: true,
  },
}

export const WithIcon: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Button>
        <Circle />
        With left icon
      </Button>
      <Button>
        With right icon
        <Circle />
      </Button>
      <Button>
        <Circle />
        Both
        <Circle />
      </Button>
    </div>
  ),
}

export const IconOnly: Story = {
  render: () => (
    <div className="flex flex-wrap items-center gap-3">
      <Button size="icon" aria-label="Add item" variant="default">
        <Plus />
      </Button>
      <Button size="icon" aria-label="Add item" variant="secondary">
        <Plus />
      </Button>
      <Button size="icon" aria-label="Add item" variant="outline">
        <Plus />
      </Button>
      <Button size="icon" aria-label="Add item" variant="ghost">
        <Plus />
      </Button>
    </div>
  ),
}

export const LongLabel: Story = {
  args: {
    children: 'Confirm and continue to the next step of onboarding',
  },
}

/** Tab to the button to verify focus-visible ring (custom/outline). */
export const FocusVisible: Story = {
  render: () => (
    <div className="flex flex-col gap-3">
      <p className="text-sm text-muted-foreground">
        Press Tab to move focus onto the button and confirm the 3px focus ring.
      </p>
      <Button>Focus me</Button>
    </div>
  ),
  parameters: {
    a11y: {
      test: 'todo',
    },
  },
}
