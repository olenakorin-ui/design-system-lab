import * as React from 'react'
import { ChevronLeft, ChevronRight, MoreHorizontal } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'

function Pagination({ className, ...props }: React.ComponentProps<'nav'>) {
  return (
    <nav
      data-slot="pagination"
      role="navigation"
      aria-label="Pagination"
      className={cn('mx-auto flex w-full justify-center', className)}
      {...props}
    />
  )
}

function PaginationContent({ className, ...props }: React.ComponentProps<'ul'>) {
  return (
    <ul
      data-slot="pagination-content"
      className={cn('flex flex-row items-center gap-1', className)}
      {...props}
    />
  )
}

function PaginationItem({ className, ...props }: React.ComponentProps<'li'>) {
  return <li data-slot="pagination-item" className={cn('', className)} {...props} />
}

type PaginationLinkProps = React.ComponentProps<'button'> & {
  isActive?: boolean
}

function PaginationLink({ className, isActive, ...props }: PaginationLinkProps) {
  return (
    <Button
      type="button"
      data-slot="pagination-link"
      data-active={isActive ? 'true' : undefined}
      aria-current={isActive ? 'page' : undefined}
      variant={isActive ? 'outline' : 'ghost'}
      size="icon"
      className={cn(className)}
      {...props}
    />
  )
}

function PaginationPrevious({
  className,
  ...props
}: React.ComponentProps<typeof Button>) {
  return (
    <Button
      type="button"
      data-slot="pagination-previous"
      variant="ghost"
      className={cn('gap-1 px-2.5 sm:pr-4', className)}
      {...props}
    >
      <ChevronLeft aria-hidden="true" />
      <span>Previous</span>
    </Button>
  )
}

function PaginationNext({ className, ...props }: React.ComponentProps<typeof Button>) {
  return (
    <Button
      type="button"
      data-slot="pagination-next"
      variant="ghost"
      className={cn('gap-1 px-2.5 sm:pl-4', className)}
      {...props}
    >
      <span>Next</span>
      <ChevronRight aria-hidden="true" />
    </Button>
  )
}

function PaginationEllipsis({ className, ...props }: React.ComponentProps<'span'>) {
  return (
    <span
      data-slot="pagination-ellipsis"
      aria-hidden="true"
      className={cn('flex size-9 items-center justify-center text-foreground', className)}
      {...props}
    >
      <MoreHorizontal className="size-4" />
      <span className="sr-only">More pages</span>
    </span>
  )
}

export {
  Pagination,
  PaginationContent,
  PaginationItem,
  PaginationLink,
  PaginationPrevious,
  PaginationNext,
  PaginationEllipsis,
}
export type { PaginationLinkProps }
