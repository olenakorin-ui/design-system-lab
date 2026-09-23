import type { Meta, StoryObj } from '@storybook/react-vite'
import { useState } from 'react'

import {
  AccessRequestReview,
  type LoadState,
} from '@/prototypes/access-request-review/AccessRequestReview'

const meta = {
  title: 'Prototypes/Access Request Review',
  component: AccessRequestReview,
  parameters: { layout: 'fullscreen' },
  tags: ['autodocs'],
} satisfies Meta<typeof AccessRequestReview>

export default meta
type Story = StoryObj<typeof meta>

export const PendingReviewer: Story = {
  args: {
    initialStatus: 'pending',
    role: 'reviewer',
    loadState: 'loaded',
  },
}

export const Approved: Story = {
  args: {
    initialStatus: 'approved',
    role: 'reviewer',
  },
}

export const Rejected: Story = {
  args: {
    initialStatus: 'rejected',
    role: 'reviewer',
  },
}

export const ViewerReadOnly: Story = {
  args: {
    initialStatus: 'pending',
    role: 'viewer',
  },
}

export const ErrorState: Story = {
  render: () => {
    const [loadState, setLoadState] = useState<LoadState>('error')
    return (
      <AccessRequestReview
        loadState={loadState}
        onRetry={() => setLoadState('loaded')}
      />
    )
  },
}

export const LongNames: Story = {
  args: {
    initialStatus: 'pending',
    role: 'reviewer',
    longNames: true,
  },
}

export const DarkMode: Story = {
  globals: { theme: 'dark' },
  args: {
    initialStatus: 'pending',
    role: 'reviewer',
  },
}

export const NarrowViewport: Story = {
  parameters: {
    viewport: { defaultViewport: 'mobile1' },
  },
  args: {
    initialStatus: 'pending',
    role: 'reviewer',
    longNames: true,
  },
}
