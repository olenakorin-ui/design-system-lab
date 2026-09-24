import type { Meta, StoryObj } from '@storybook/react-vite'

import { Skeleton } from '@/components/ui/skeleton'

const meta = {
  title: 'Components/Skeleton',
  component: Skeleton,
  parameters: { layout: 'padded' },
  tags: ['autodocs'],
} satisfies Meta<typeof Skeleton>

export default meta
type Story = StoryObj<typeof meta>

export const Line: Story = {
  render: () => <Skeleton className="h-4 w-[180px]" />,
}

export const Block: Story = {
  render: () => <Skeleton className="h-32 w-full max-w-sm rounded-md" />,
}

export const MultipleLines: Story = {
  render: () => (
    <div className="flex w-full max-w-sm flex-col gap-2" aria-busy="true" aria-label="Loading">
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-5/6" />
      <Skeleton className="h-4 w-2/3" />
    </div>
  ),
}

export const TableRows: Story = {
  render: () => (
    <div
      className="flex w-full max-w-xl flex-col gap-3"
      aria-busy="true"
      aria-label="Loading table"
    >
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className="flex items-center gap-3">
          <Skeleton className="size-4 shrink-0 rounded-sm" />
          <Skeleton className="h-4 flex-1" />
          <Skeleton className="h-4 w-24" />
          <Skeleton className="h-4 w-16" />
        </div>
      ))}
    </div>
  ),
}

export const DarkMode: Story = {
  globals: { theme: 'dark' },
  render: () => (
    <div className="flex w-full max-w-sm flex-col gap-3" aria-busy="true" aria-label="Loading">
      <div className="flex items-center gap-3">
        <Skeleton className="size-10 shrink-0 rounded-full" />
        <div className="flex flex-1 flex-col gap-2">
          <Skeleton className="h-4 w-3/4" />
          <Skeleton className="h-4 w-1/2" />
        </div>
      </div>
      <Skeleton className="h-24 w-full" />
    </div>
  ),
}
