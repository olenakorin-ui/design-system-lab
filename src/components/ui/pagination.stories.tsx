import type { Meta, StoryObj } from '@storybook/react-vite'
import { useState } from 'react'

import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from '@/components/ui/pagination'

const meta = {
  title: 'Components/Pagination',
  component: Pagination,
  parameters: { layout: 'centered' },
  tags: ['autodocs'],
} satisfies Meta<typeof Pagination>

export default meta
type Story = StoryObj<typeof meta>

function PaginationDemo({
  page,
  total,
}: {
  page: number
  total: number
}) {
  const [current, setCurrent] = useState(page)
  const pages = Array.from({ length: total }, (_, i) => i + 1)
  const showEllipsis = total > 5

  return (
    <Pagination>
      <PaginationContent>
        <PaginationItem>
          <PaginationPrevious
            aria-label="Go to previous page"
            disabled={current <= 1}
            onClick={() => setCurrent((p) => Math.max(1, p - 1))}
          />
        </PaginationItem>
        {showEllipsis ? (
          <>
            <PaginationItem>
              <PaginationLink
                isActive={current === 1}
                aria-label="Page 1"
                onClick={() => setCurrent(1)}
              >
                1
              </PaginationLink>
            </PaginationItem>
            {current > 3 ? (
              <PaginationItem>
                <PaginationEllipsis />
              </PaginationItem>
            ) : null}
            {pages
              .filter((p) => p !== 1 && p !== total && Math.abs(p - current) <= 1)
              .map((p) => (
                <PaginationItem key={p}>
                  <PaginationLink
                    isActive={current === p}
                    aria-label={`Page ${p}`}
                    onClick={() => setCurrent(p)}
                  >
                    {p}
                  </PaginationLink>
                </PaginationItem>
              ))}
            {current < total - 2 ? (
              <PaginationItem>
                <PaginationEllipsis />
              </PaginationItem>
            ) : null}
            <PaginationItem>
              <PaginationLink
                isActive={current === total}
                aria-label={`Page ${total}`}
                onClick={() => setCurrent(total)}
              >
                {total}
              </PaginationLink>
            </PaginationItem>
          </>
        ) : (
          pages.map((p) => (
            <PaginationItem key={p}>
              <PaginationLink
                isActive={current === p}
                aria-label={`Page ${p}`}
                onClick={() => setCurrent(p)}
              >
                {p}
              </PaginationLink>
            </PaginationItem>
          ))
        )}
        <PaginationItem>
          <PaginationNext
            aria-label="Go to next page"
            disabled={current >= total}
            onClick={() => setCurrent((p) => Math.min(total, p + 1))}
          />
        </PaginationItem>
      </PaginationContent>
    </Pagination>
  )
}

export const FirstPage: Story = {
  render: () => <PaginationDemo page={1} total={5} />,
}

export const MiddlePage: Story = {
  render: () => <PaginationDemo page={3} total={5} />,
}

export const LastPage: Story = {
  render: () => <PaginationDemo page={5} total={5} />,
}

export const ManyPages: Story = {
  render: () => <PaginationDemo page={6} total={12} />,
}

export const DarkMode: Story = {
  globals: { theme: 'dark' },
  render: () => <PaginationDemo page={2} total={5} />,
}
