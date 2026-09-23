import type { Meta, StoryObj } from '@storybook/react-vite'

import { AccessRequestReview } from '@/prototypes/access-request-review/components/AccessRequestReview'
import { getAccessRequestScenario } from '@/prototypes/access-request-review/mocks/scenarios'

/**
 * Regression-only Storybook coverage for the Access Request Review UI.
 * Primary runtime and sharing: Prototype Lab (`npm run dev` → /prototypes/access-request).
 */
const meta = {
  title: 'Prototypes/Access Request Review (regression)',
  component: AccessRequestReview,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component:
          'Internal regression story. Use the Prototype Lab app to run and share this product flow.',
      },
    },
  },
  tags: ['autodocs'],
} satisfies Meta<typeof AccessRequestReview>

export default meta
type Story = StoryObj<typeof meta>

function fromScenario(id: Parameters<typeof getAccessRequestScenario>[0]) {
  const s = getAccessRequestScenario(id)
  return {
    requestId: s.requestId,
    initialStatus: s.initialStatus,
    role: s.role,
    loadState: s.loadState,
    longNames: s.longNames,
    requestor: s.requestor,
    department: s.department,
    system: s.system,
    defaultAccessLevel: s.accessLevelDefault,
    defaultTicket: s.referenceTicket,
  }
}

export const PendingReviewer: Story = {
  args: fromScenario('pending'),
}

export const Approved: Story = {
  args: fromScenario('approved'),
}

export const Rejected: Story = {
  args: fromScenario('rejected'),
}

export const ViewerReadOnly: Story = {
  args: fromScenario('viewer'),
}

export const ErrorState: Story = {
  args: fromScenario('error'),
}

export const LongNames: Story = {
  args: {
    ...fromScenario('pending'),
    longNames: true,
    requestor: undefined,
    department: undefined,
    system: undefined,
  },
}

export const DarkMode: Story = {
  globals: { theme: 'dark' },
  args: fromScenario('pending'),
}

export const NarrowViewport: Story = {
  parameters: {
    viewport: { defaultViewport: 'mobile1' },
  },
  args: fromScenario('pending'),
}
