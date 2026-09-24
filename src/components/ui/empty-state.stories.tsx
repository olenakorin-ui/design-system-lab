import type { Meta, StoryObj } from '@storybook/react-vite'
import { Inbox, Search } from 'lucide-react'

import { Button } from '@/components/ui/button'
import {
  EmptyState,
  EmptyStateActions,
  EmptyStateDescription,
  EmptyStateHeader,
  EmptyStateIcon,
  EmptyStateTitle,
} from '@/components/ui/empty-state'

const meta = {
  title: 'Components/EmptyState',
  component: EmptyState,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
} satisfies Meta<typeof EmptyState>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  render: () => (
    <EmptyState>
      <EmptyStateIcon>
        <Inbox aria-hidden="true" />
      </EmptyStateIcon>
      <EmptyStateHeader>
        <EmptyStateTitle>No items yet</EmptyStateTitle>
        <EmptyStateDescription>
          When content is available, it will appear here.
        </EmptyStateDescription>
      </EmptyStateHeader>
    </EmptyState>
  ),
}

export const WithAction: Story = {
  render: () => (
    <EmptyState>
      <EmptyStateIcon>
        <Inbox aria-hidden="true" />
      </EmptyStateIcon>
      <EmptyStateHeader>
        <EmptyStateTitle>No items yet</EmptyStateTitle>
        <EmptyStateDescription>
          When content is available, it will appear here.
        </EmptyStateDescription>
      </EmptyStateHeader>
      <EmptyStateActions>
        <Button type="button">Primary action</Button>
        <Button type="button" variant="outline">
          Secondary action
        </Button>
      </EmptyStateActions>
    </EmptyState>
  ),
}

export const SearchNoResults: Story = {
  render: () => (
    <EmptyState>
      <EmptyStateIcon>
        <Search aria-hidden="true" />
      </EmptyStateIcon>
      <EmptyStateHeader>
        <EmptyStateTitle>No results found</EmptyStateTitle>
        <EmptyStateDescription>
          Try adjusting search or filters to find what you need.
        </EmptyStateDescription>
      </EmptyStateHeader>
      <EmptyStateActions>
        <Button type="button" variant="outline">
          Clear filters
        </Button>
      </EmptyStateActions>
    </EmptyState>
  ),
}

export const WithoutIcon: Story = {
  render: () => (
    <EmptyState>
      <EmptyStateHeader>
        <EmptyStateTitle>Nothing to show</EmptyStateTitle>
        <EmptyStateDescription>
          This composition omits the optional icon slot.
        </EmptyStateDescription>
      </EmptyStateHeader>
      <EmptyStateActions>
        <Button type="button">Continue</Button>
      </EmptyStateActions>
    </EmptyState>
  ),
}

export const LongContent: Story = {
  render: () => (
    <EmptyState>
      <EmptyStateIcon>
        <Inbox aria-hidden="true" />
      </EmptyStateIcon>
      <EmptyStateHeader>
        <EmptyStateTitle>
          No matching records for this unusually long heading that should wrap without breaking
          layout
        </EmptyStateTitle>
        <EmptyStateDescription>
          Descriptions can also run long. The empty pattern keeps a readable measure inside the
          dashed container while remaining a non-error, informational surface — not an Alert.
        </EmptyStateDescription>
      </EmptyStateHeader>
      <EmptyStateActions>
        <Button type="button">Primary action</Button>
      </EmptyStateActions>
    </EmptyState>
  ),
}

export const DarkMode: Story = {
  globals: { theme: 'dark' },
  render: () => (
    <EmptyState>
      <EmptyStateIcon>
        <Inbox aria-hidden="true" />
      </EmptyStateIcon>
      <EmptyStateHeader>
        <EmptyStateTitle>No items yet</EmptyStateTitle>
        <EmptyStateDescription>
          When content is available, it will appear here.
        </EmptyStateDescription>
      </EmptyStateHeader>
      <EmptyStateActions>
        <Button type="button">Primary action</Button>
        <Button type="button" variant="outline">
          Secondary action
        </Button>
      </EmptyStateActions>
    </EmptyState>
  ),
}
